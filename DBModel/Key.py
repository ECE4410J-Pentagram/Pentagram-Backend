from peewee import CharField, ForeignKeyField
from .db import BaseModel
from .User import User

class Key(BaseModel):
    name = CharField(max_length=1024)
    pk = CharField(max_length=2048)
    owner = ForeignKeyField(User, backref='keys')