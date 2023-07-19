from DBModel.db import psql_db
from DBModel.User import User
from DBModel.Key import Key
from DBModel.Device import Device, Owener_Device_Relationship

def create_tables():
    with psql_db:
        psql_db.create_tables([User, Key, Device, Owener_Device_Relationship])

if __name__ == "__main__":
    create_tables()
