from litestar.config.cors import CORSConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.plugins.prometheus import PrometheusConfig
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig

from app.core.settings import settings

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.database_url,
    session_config=session_config,
)
cors_config = CORSConfig(
    allow_origins=settings.origins,
    allow_credentials=True,
)
rate_limit_config = RateLimitConfig(rate_limit=("minute", 50), exclude=["/schema"])
prometheus_config = PrometheusConfig()
