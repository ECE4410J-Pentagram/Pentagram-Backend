from fastapi import Depends
from DBModel import db
from DBModel.db import db_state_default
async def reset_db_state():
    db.psql_db._state._state.set(db_state_default.copy())
    db.psql_db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.psql_db.connect()
        yield
    finally:
        if not db.psql_db.is_closed():
            db.psql_db.close()

