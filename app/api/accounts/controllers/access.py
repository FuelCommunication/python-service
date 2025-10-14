from litestar import Controller, Request, Response, post
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.status_codes import HTTP_201_CREATED, HTTP_409_CONFLICT

from ..deps import provide_user_repo
from ..guards import auth, create_auth_response
from ..repositories import UserRepository
from ..schemas import AuthBody, LoginAccount, RegisterAccount, UserReadDto


class AccessController(Controller):
    """User login and registration"""

    path = "/access"
    tags = ["Access"]
    dependencies = {"users_repo": Provide(provide_user_repo)}
    return_dto = UserReadDto

    @post(path="/login")
    async def login(self, data: LoginAccount, users_repo: UserRepository) -> Response[AuthBody]:
        """Login account"""
        user = await users_repo.check_email_and_password(email=str(data.email), password=data.password)
        if not user:
            raise NotFoundException(detail="User not found")

        return create_auth_response(user)

    @post(path="/register", status_code=HTTP_201_CREATED)
    async def register(self, data: RegisterAccount, users_repo: UserRepository) -> Response[AuthBody]:
        """Create a new user"""
        user = await users_repo.get_by_email(email=str(data.email))
        if user:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="User is already exist")
        user = await users_repo.create(data=data)
        return create_auth_response(user)

    @post(path="/logout")
    async def logout(self, request: Request) -> Response:
        """Account logout"""
        request.cookies.pop(auth.key, None)
        request.clear_session()
        response = Response({"message": "OK"}, status_code=200)
        response.delete_cookie(auth.key)

        return response
