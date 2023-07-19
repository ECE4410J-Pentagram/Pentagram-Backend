from peewee import CharField, ForeignKeyField
from .db import BaseModel
from .User import User

class Device(BaseModel):
    device_id = CharField(max_length=1024)
    owner = ForeignKeyField(User, backref='keys')
