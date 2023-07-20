from DBModel.db import psql_db
from DBModel.Device import Device
from DBModel.Key import Key
from DBModel.Relationship import Relationship

def create_tables():
    with psql_db:
        psql_db.create_tables([Device, Key, Relationship])

if __name__ == "__main__":
    create_tables()
