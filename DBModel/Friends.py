from peewee import CharField, ForeignKeyField
from .db import BaseModel


class Friend(BaseModel):
    user1 = ForeignKeyField("User", backref="friends")
    user2 = ForeignKeyField("User", backref="friends")

    def __str__(self):
        return f"User: {self.user1} with public key: {self.user2}"

    def __repr__(self):
        return self.__str__()
