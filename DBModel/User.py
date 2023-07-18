import bcrypt
from .db import BaseModel
from peewee import CharField
import hashlib
from config import config

class User(BaseModel):
    username = CharField(unique=True)
    hashed_password = CharField()
    password_salt = CharField()
    password_algo = CharField()

    def __str__(self):
        return f"User: {self.username}"

    def __repr__(self):
        return self.__str__()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_salt = bcrypt.gensalt().decode()
        self.password_algo = config.DEFAULT_HASH
        password = kwargs.get("password")
        if password:
            self.hashed_password = self._hash_password(password)

    def _hash_password(self, password):
        salted_password = password + self.password_salt
        hasher = hashlib.new(str(self.password_algo))
        hasher.update(salted_password.encode())
        hashed_password = hasher.hexdigest()
        return hashed_password

    def check_password(self, password):
        hashed_password = self._hash_password(password)
        return hashed_password == self.hashed_password
        
