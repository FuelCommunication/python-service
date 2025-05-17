from litestar import Litestar
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin

from app.config import cors_config, db_config, rate_limit_config

app = Litestar(
    middleware=[rate_limit_config.middleware],
    plugins=[SQLAlchemyPlugin(config=db_config)],
    cors_config=cors_config,
    debug=True,
)
