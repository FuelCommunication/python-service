from litestar.config.cors import CORSConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.plugins.sqlalchemy import AsyncSessionConfig, SQLAlchemyAsyncConfig

session_config = AsyncSessionConfig(expire_on_commit=False)
db_config = SQLAlchemyAsyncConfig(
    connection_string="postgresql+asyncpg://postgres:postgres@localhost:5433/test_db",
    session_config=session_config,
)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

cors_config = CORSConfig(
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_credentials=True,
)

rate_limit_config = RateLimitConfig(rate_limit=("minute", 50), exclude=["/schema"])
