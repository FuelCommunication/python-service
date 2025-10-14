from litestar import Response
from litestar.connection import ASGIConnection
from litestar.exceptions import PermissionDeniedException
from litestar.handlers import BaseRouteHandler
from litestar.security.jwt import OAuth2PasswordBearerAuth, Token

import app.db.models as m
from app.core.config import sqlalchemy_config
from app.core.settings import settings

from .deps import provide_user_repo
from .schemas import AuthBody


def requires_verified_user(connection: ASGIConnection[m.User, any, any, any], _: BaseRouteHandler) -> None:
    """Verify the connection user is a superuser"""
    if connection.user.is_verified:
        return
    raise PermissionDeniedException(detail="User account is not verified")


async def current_user_from_token(token: Token, connection: ASGIConnection[any, any, any, any]) -> m.User | None:
    """Lookup current user from local JWT token"""
    users_repo = await provide_user_repo(sqlalchemy_config.provide_session(connection.app.state, connection.scope))
    user = await users_repo.get_by_email(email=token.sub)
    return user


auth = OAuth2PasswordBearerAuth[m.User](
    retrieve_user_handler=current_user_from_token,
    token_secret=settings.SECRET_KEY,
    token_url="/login",
    exclude=["/login", "/schema", "/ping", "/access/register"],
)


def create_auth_response(user: m.User) -> Response[AuthBody]:
    session = auth.login(user.email)
    body = AuthBody(session=session.content, user=user)

    response = Response(
        content=body,
        media_type=session.media_type,
        status_code=session.status_code,
        headers=session.headers,
        cookies=session.cookies,
    )
    return response
