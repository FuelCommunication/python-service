from uuid import UUID

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, delete, get, patch
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_201_CREATED

import app.db.models as m

from ..deps import provide_user_repo
from ..repositories import UserRepository
from ..schemas import UserReadDto, UserUpdatePartial


class UserController(Controller):
    """User Account Controller"""

    path = "/users"
    tags = ["User Accounts"]
    dependencies = {"users_repo": Provide(provide_user_repo)}
    return_dto = UserReadDto

    @get(path="/{user_id:uuid}")
    async def get(self, user_id: UUID, users_repo: UserRepository) -> m.User:
        """Get an existing user"""
        try:
            user = await users_repo.get(user_id)
            return user
        except NotFoundError:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

    @patch(path="/{user_id:uuid}", status_code=HTTP_201_CREATED)
    async def partial_update(self, user_id: UUID, data: UserUpdatePartial, users_repo: UserRepository) -> m.User:
        """Update a user"""
        try:
            user = await users_repo.update_partial(user_id=user_id, data=data)
            return user
        except NotFoundError:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

    @delete(path="/{user_id:uuid}")
    async def delete(self, user_id: UUID, users_repo: UserRepository) -> None:
        """Delete an existing user"""
        try:
            await users_repo.delete(user_id, auto_commit=True)
        except NotFoundError:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
