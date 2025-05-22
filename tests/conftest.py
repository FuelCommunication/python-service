from collections.abc import AsyncIterator

import pytest_asyncio
from litestar import Litestar
from litestar.testing import AsyncTestClient

from app.main import app


@pytest_asyncio.fixture(name="client")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app) as client:
        yield client
