from .models import InfoDevice, Key
from DBModel.Device import Device
from DBModel.Key import Key as DBKey

def infodevice(name: str):
    db_device = Device.get_or_none(Device.name == name)
    if db_device is None:
        return None
    keys = DBKey.select().where(DBKey.owner == db_device)
    keys = [Key(name=key.name, pk=key.pk) for key in keys]
    return InfoDevice(name=db_device.name, keys=keys)

