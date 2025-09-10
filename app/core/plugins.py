from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from litestar_granian import GranianPlugin

from app.core.config import sqlalchemy_config

sqlalchemy = SQLAlchemyPlugin(config=sqlalchemy_config)
granian = GranianPlugin()
