from peewee import CharField, ForeignKeyField
from .db import BaseModel
from .User import User

class Device(BaseModel):
    name = CharField(max_length=1024)
    key = CharField(max_length=1024)

class Owener_Device_Relationship(BaseModel):
    device = ForeignKeyField(Device, backref='devices')
    user = ForeignKeyField(User, backref='users')


def select_all_devices_by_user(user: User):
    return Device.select(Device, Owener_Device_Relationship).join(Owener_Device_Relationship).where(Owener_Device_Relationship.user == user)

def select_device_by_user_name(user: User, device_name: str):
    return select_all_devices_by_user(user).where(Device.name == device_name).first()
