from DBModel.db import psql_db
from DBModel.Device import Device

def create_tables():
    with psql_db:
        psql_db.create_tables([Device, ])

if __name__ == "__main__":
    create_tables()
