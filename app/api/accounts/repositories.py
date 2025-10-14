from uuid import UUID

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from litestar.exceptions import PermissionDeniedException
from sqlalchemy import select

import app.db.models as m
from app.utils.password import check_password, hash_password

from .schemas import RegisterAccount, UserUpdatePartial


class UserRepository(SQLAlchemyAsyncRepository[m.User]):
    model_type = m.User

    async def create(self, *, data: RegisterAccount) -> m.User:
        user = m.User(**data.model_dump(exclude_unset=True, exclude_none=True))
        user.password = hash_password(data.password)
        obj = await self.add(user)
        await self.session.commit()
        return obj

    async def get_by_email(self, *, email: str) -> m.User | None:
        stmt = select(self.model_type).where(self.model_type.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def check_email_and_password(self, *, email: str, password: str) -> m.User | None:
        user = await self.get_by_email(email=email)
        if user is None:
            return None

        result = check_password(password, user.password)
        if not result:
            return None

        return user

    async def update_partial(self, *, user_id: UUID, data: UserUpdatePartial) -> m.User:
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": user_id})

        obj = await self.update(m.User(**raw_obj))
        await self.session.commit()
        return obj

    async def update_password(self, *, old_password: str, new_password: str, user: m.User):
        """Modify stored user password"""

        if user.password is None:
            msg = "User not found or password invalid."
            raise PermissionDeniedException(detail=msg)
        if not check_password(old_password, user.password):
            msg = "User not found or password invalid."
            raise PermissionDeniedException(detail=msg)

        user.password = hash_password(new_password)
        await self.update(user)
