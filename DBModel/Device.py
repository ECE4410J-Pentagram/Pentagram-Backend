from peewee import CharField, ForeignKeyField
from .db import BaseModel
import bcrypt

class Device(BaseModel):
    name = CharField(max_length=1024)
    key = CharField(max_length=1024, unique=True)

