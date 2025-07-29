from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import HTTPException, NotFoundException
from litestar.status_codes import HTTP_201_CREATED, HTTP_409_CONFLICT
from pydantic import UUID7

from ..deps import provide_user_repo
from ..repositories import UserRepository
from ..schemas import CreateUser, User, UserReadDto, UserUpdatePartial


class UserController(Controller):
    """User Account Controller"""

    path = "/users"
    tags = ["User Accounts"]
    dependencies = {"users_repo": Provide(provide_user_repo)}
    return_dto = UserReadDto

    @post(status_code=HTTP_201_CREATED, guards=None)
    async def create(self, data: CreateUser, users_repo: UserRepository) -> User:
        """Create a new user"""

        user = await users_repo.get_by_email(email=data.email.__str__())
        if user:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="User is already exist")

        obj = await users_repo.create(data=data)
        return User.model_validate(obj)

    @get(path="/{user_id:uuid}")
    async def get(self, user_id: UUID7, users_repo: UserRepository) -> User:
        """Get an existing user"""

        try:
            obj = await users_repo.get(user_id)
            return User.model_validate(obj)
        except NotFoundError:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

    @patch(path="/{user_id:uuid}", status_code=HTTP_201_CREATED)
    async def partial_update(self, user_id: UUID7, data: UserUpdatePartial, users_repo: UserRepository) -> User:
        """Update a user"""

        try:
            obj = await users_repo.update_partial(user_id=user_id, data=data)
            return User.model_validate(obj)
        except NotFoundError:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

    @delete(path="/{user_id:uuid}")
    async def delete(self, user_id: UUID7, users_repo: UserRepository) -> None:
        """Delete an existing user"""

        try:
            await users_repo.delete(user_id)
        except NotFoundError:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
