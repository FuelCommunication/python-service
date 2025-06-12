from uuid import UUID

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from pydantic import EmailStr
from sqlalchemy import select

from app.models import AccountModel
from app.utils.password import check_password, hash_password

from .schemas import AccountUpdatePartial, CreateAccount, GetAccount


class AccountRepository(SQLAlchemyAsyncRepository[AccountModel]):
    model_type = AccountModel

    async def create(self, *, data: CreateAccount) -> AccountModel:
        account = AccountModel(**data.model_dump(exclude_unset=True, exclude_none=True))
        account.password = hash_password(data.password)
        obj = await self.add(account)
        await self.session.commit()
        return obj

    async def get_by_email(self, *, email: EmailStr) -> AccountModel | None:
        stmt = select(self.model_type).where(self.model_type.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_partial(self, *, account_id: UUID, data=AccountUpdatePartial) -> AccountModel:
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": account_id})
        obj = await self.update(AccountModel(**raw_obj))
        await self.session.commit()
        return obj

    async def check_email_and_password(self, data: GetAccount) -> AccountModel | None:
        account = await self.get_by_email(email=data.email)
        if account is None:
            return None

        result = check_password(data.password, account.password)
        if result is False:
            return None

        return account
