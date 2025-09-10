from collections.abc import AsyncGenerator
from typing import Any

from fast_depends import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.api.accounts.repositories import UserRepository
from app.core.config import sqlalchemy_config

async_session_maker = async_sessionmaker(sqlalchemy_config.get_engine(), expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_maker() as session:
        yield session


async def get_users_repo(session: AsyncSession = Depends(get_db_session)):
    return UserRepository(session=session)
