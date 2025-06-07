from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from litestar_granian import GranianPlugin

from app.core.config import db_config

sqlalchemy = SQLAlchemyPlugin(config=db_config)
granian = GranianPlugin()
