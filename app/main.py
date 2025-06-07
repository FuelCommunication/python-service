from litestar import Litestar

from app.api import api_routers
from app.core.config import cors_config, db_config, rate_limit_config
from app.core.plugins import granian, sqlalchemy


async def on_startup() -> None:
    from litestar.plugins.sqlalchemy import base

    """Initializes the models."""
    async with db_config.get_engine().begin() as conn:
        await conn.run_sync(base.UUIDBase.metadata.create_all)


app = Litestar(
    route_handlers=[api_routers],
    middleware=[rate_limit_config.middleware],
    plugins=[sqlalchemy, granian],
    cors_config=cors_config,
    on_startup=[on_startup],
)
