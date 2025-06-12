from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import AccountRepository


async def provide_accounts_repo(db_session: AsyncSession) -> AccountRepository:
    return AccountRepository(session=db_session)
