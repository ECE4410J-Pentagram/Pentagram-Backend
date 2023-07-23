from peewee import PostgresqlDatabase, Model
from contextvars import ContextVar
import peewee
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


db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())
class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]

psql_db._state = PeeweeConnectionState()

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

