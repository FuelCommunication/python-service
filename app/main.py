from litestar import Litestar

from app.api import api_routers
from app.config import cors_config, rate_limit_config
from app.plugins import granian, sql_alchemy

app = Litestar(
    route_handlers=[api_routers],
    middleware=[rate_limit_config.middleware],
    plugins=[sql_alchemy, granian],
    cors_config=cors_config,
    debug=True,
)
