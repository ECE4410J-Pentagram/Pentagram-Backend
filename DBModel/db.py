from peewee import PostgresqlDatabase, Model
from config import config
from playhouse.pool import PooledPostgresqlDatabase

psql_db = PooledPostgresqlDatabase(
    database=config.PDB_NAME,
    user=config.PDB_USER,
    password=config.PDB_PASS,
    host=config.PDB_HOST,
    port=config.PDB_PORT,
    max_connections=8,
    stale_timeout=300
)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

