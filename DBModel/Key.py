from peewee import CharField, ForeignKeyField
import hashlib
from config import config
from .db import BaseModel

class Key(BaseModel):
    name = CharField
    pk = CharField
    owner = ForeignKeyField('User', backref='keys')
