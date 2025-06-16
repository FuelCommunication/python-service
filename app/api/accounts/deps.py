from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import UserRepository


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)
