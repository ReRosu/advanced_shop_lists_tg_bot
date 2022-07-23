from databases import Database
from sqlalchemy import MetaData, create_engine
from source.core.settings import load_db_config

db_cfg = load_db_config("db/db_config/db.ini")
db_url = db_cfg.db_url

metadata = MetaData()
db = Database(db_url)
engine = create_engine(db_url)
