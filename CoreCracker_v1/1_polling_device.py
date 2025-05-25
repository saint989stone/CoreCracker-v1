from module_database.database import Database
from module_config.config import settings

db = Database(*settings.db_url_pg_psycorg)
db.create_engine()
#db.insert_data('device', data)
result = db.select_where_data('device')