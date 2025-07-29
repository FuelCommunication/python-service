from litestar.connection import ASGIConnection
from litestar.exceptions import PermissionDeniedException
from litestar.handlers import BaseRouteHandler
from litestar.security.jwt import OAuth2PasswordBearerAuth, Token

from app.core.config import db_config
from app.core.settings import settings
from app.models import UserModel

from .deps import provide_user_repo


def requires_verified_user(connection: ASGIConnection[UserModel, any, any, any], _: BaseRouteHandler) -> None:
    """Verify the connection user is a superuser"""
    if connection.user.is_verified:
        return
    raise PermissionDeniedException(detail="User account is not verified")


async def current_user_from_token(token: Token, connection: ASGIConnection[any, any, any, any]) -> UserModel | None:
    """Lookup current user from local JWT token"""
    users_repo = await provide_user_repo(db_config.provide_session(connection.app.state, connection.scope))
    user = await users_repo.get_by_email(email=token.sub)
    return user


auth = OAuth2PasswordBearerAuth[UserModel](
    retrieve_user_handler=current_user_from_token,
    token_secret=settings.SECRET_KEY,
    token_url="/login",
    exclude=["/login", "/schema", "/ping"],
)
