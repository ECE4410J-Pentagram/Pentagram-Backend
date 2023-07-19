from peewee import CharField, ForeignKeyField
from .db import BaseModel
from .Device import Device

class Key(BaseModel):
    name = CharField(max_length=1024)
    pk = CharField(max_length=2048)
    owner = ForeignKeyField(Device, backref='keys')
