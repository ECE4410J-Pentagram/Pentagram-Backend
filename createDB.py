from DBModel.db import psql_db
from DBModel.User import User

def create_tables():
    with psql_db:
        psql_db.create_tables([User])

if __name__ == "__main__":
    create_tables()
