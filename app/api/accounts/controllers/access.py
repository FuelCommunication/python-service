from litestar import Controller, Request, Response, post
from litestar.di import Provide
from litestar.exceptions import NotFoundException

from ..deps import provide_user_repo
from ..guards import auth
from ..repositories import UserRepository
from ..schemas import GetUser, LoginResponse, User


class AccessController(Controller):
    """User login and registration"""

    tags = ["Access"]
    dependencies = {"users_repo": Provide(provide_user_repo)}

    @post(path="/login")
    async def login(self, data: GetUser, users_repo: UserRepository) -> LoginResponse:
        """Login account"""

        user = await users_repo.check_email_and_password(data=data)
        if not user:
            raise NotFoundException(detail="User not found")

        session = auth.login(user.email)
        return LoginResponse(session=session.content, user=User.model_validate(user))

    @post(path="/logout")
    async def logout(self, request: Request) -> Response:
        """Account logout"""
        request.cookies.pop(auth.key, None)
        request.clear_session()

        response = Response({"message": "OK"}, status_code=200)
        response.delete_cookie(auth.key)

        return response
