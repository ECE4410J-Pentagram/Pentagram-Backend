from peewee import BooleanField, ForeignKeyField
from .db import BaseModel


class Friend(BaseModel):
    user1 = ForeignKeyField("User", backref="friends")
    user2 = ForeignKeyField("User", backref="friends")
    is_accepted = BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user1} with public key: {self.user2}"

    def __repr__(self):
        return self.__str__()
