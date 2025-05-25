from module_database.database import Database
from module_config.config import settings
import time

db = Database(*settings.db_url_pg_psycorg)
db.create_engine()
db.delete_tables()
db.create_tables()
