import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
async def test_ping(client: AsyncTestClient[Litestar]) -> None:
    response = await client.get("/ping")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"ping": "pong"}
