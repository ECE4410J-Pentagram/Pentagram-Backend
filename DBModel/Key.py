from peewee import CharField, ForeignKeyField
from .db import BaseModel

class Key(BaseModel):
    name = CharField
    pk = CharField
    owner = ForeignKeyField('User', backref='keys')
