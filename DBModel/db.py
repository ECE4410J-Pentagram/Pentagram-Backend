from peewee import PostgresqlDatabase, Model
from config import config

psql_db = PostgresqlDatabase(
    database=config.PDB_NAME,
    user=config.PDB_USER,
    password=config.PDB_PASS,
    host=config.PDB_HOST,
)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

