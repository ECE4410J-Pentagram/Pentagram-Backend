from peewee import ForeignKeyField, BooleanField
from .db import BaseModel
from .Key import Key
from .Device import Device

class Relationship(BaseModel):
    from_key = ForeignKeyField(Key, backref='sent_relationships')
    to_device = ForeignKeyField(Device, backref='received_relationships')
    to_key = ForeignKeyField(Key, backref='received_relationships', null=True)
    pending = BooleanField(default=True)

