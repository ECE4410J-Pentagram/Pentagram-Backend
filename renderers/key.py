from fastapi import APIRouter, Depends, HTTPException
from utils.models import BaseDevice
from utils.models import BaseKey
from utils.login import loggedIn
import pydantic
from DBModel.Key import Key as DBKey
from DBModel.Device import Device

class Key(BaseKey):
    pk: str = pydantic.Field(max_length=2048)

class KeyWithOwner(Key):
    owner: BaseDevice

router = APIRouter(prefix="/api/key", tags=["key"])
@router.post("/", response_model=KeyWithOwner)
async def create_key(key: Key, device: Device = Depends(loggedIn)):
    db_key = DBKey.get_or_none(DBKey.name == key.name, DBKey.owner == device)
    if db_key is not None:
        raise HTTPException(status_code=400, detail="Key already exists")
    print(device.name)
    DBKey.create(name=key.name, pk=key.pk, owner=device)
    return KeyWithOwner(name=key.name, pk=key.pk, owner=BaseDevice(name=device.name))

@router.get("/", response_model=list[KeyWithOwner])
async def get_keys(device = Depends(loggedIn)):
    res = DBKey.select().where(DBKey.owner == device)
    res = [KeyWithOwner(name=key.name, pk=key.pk, owner=BaseDevice(name=device.name)) for key in res]
    return res

@router.get("/{key_name}", response_model=KeyWithOwner)
async def get_key(key_name: str, device = Depends(loggedIn)):
    res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == device)
    if res is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return KeyWithOwner(name=res.name, pk=res.pk, owner=BaseDevice(name=device.name))

@router.delete("/{key_name}")
async def delete_key(key_name: str, device = Depends(loggedIn)):
    res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == device)
    if res is None:
        raise HTTPException(status_code=404, detail="Key not found")
    res.delete_instance()
    return {"message": "Deleted successfully"}

@router.put("/{key_name}", response_model=KeyWithOwner)
async def update_key(key_name: str, key: Key, device = Depends(loggedIn)):
    res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == device)
    if res is None:
        raise HTTPException(status_code=404, detail="Key not found")
    res.name = key.name
    res.pk = key.pk
    res.save()
    return KeyWithOwner(name=res.name, pk=res.pk, owner=BaseDevice(name=device.name))
