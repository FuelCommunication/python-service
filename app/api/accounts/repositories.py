from uuid import UUID

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select

from app.models import UserModel
from app.utils.password import check_password, hash_password

from .schemas import CreateUser, GetUser, UserUpdatePartial


class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
    model_type = UserModel

    async def create(self, *, data: CreateUser) -> UserModel:
        user = UserModel(**data.model_dump(exclude_unset=True, exclude_none=True))
        user.password = hash_password(data.password)
        obj = await self.add(user)
        await self.session.commit()
        return obj

    async def get_by_email(self, *, email: str) -> UserModel | None:
        stmt = select(self.model_type).where(self.model_type.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_partial(self, *, user_id: UUID, data=UserUpdatePartial) -> UserModel:
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": user_id})
        obj = await self.update(UserModel(**raw_obj))
        await self.session.commit()
        return obj

    async def check_email_and_password(self, data: GetUser) -> UserModel | None:
        user = await self.get_by_email(email=data.email.__str__())
        if user is None:
            return None

        result = check_password(data.password, user.password)
        if not result:
            return None

        return user
