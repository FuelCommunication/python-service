from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from litestar_granian import GranianPlugin

from app.config import db_config

sql_alchemy = SQLAlchemyPlugin(config=db_config)
granian = GranianPlugin()
