from peewee import CharField, ForeignKeyField
from .db import BaseModel
from .User import User

class Device(BaseModel):
    name = CharField(max_length=1024)
    key = CharField(max_length=1024)

class Owener_Device_Relationship(BaseModel):
    device = ForeignKeyField(Device, backref='devices')
    user = ForeignKeyField(User, backref='users')
