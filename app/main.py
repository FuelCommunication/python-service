from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.plugins.prometheus import PrometheusController

from app.api import api_routers, auth
from app.broker.router import broker
from app.core.config import cors_config, rate_limit_config, sqlalchemy_config, prometheus_config
from app.core.plugins import granian, sqlalchemy


@asynccontextmanager
async def lifespan(_app: Litestar) -> AsyncGenerator[None]:
    from litestar.plugins.sqlalchemy import base

    """Initializes the models."""
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(base.UUIDBase.metadata.create_all)

    await broker.start()
    yield
    await broker.stop()


app = Litestar(
    route_handlers=[api_routers, PrometheusController],
    middleware=[prometheus_config.middleware, rate_limit_config.middleware],
    plugins=[sqlalchemy, granian],
    cors_config=cors_config,
    on_app_init=[auth.on_app_init],
    lifespan=[lifespan],
)
