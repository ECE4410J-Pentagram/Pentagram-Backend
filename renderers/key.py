from fastapi import APIRouter, Depends, HTTPException
from utils.models import BaseDevice
from utils.models import Key, KeyWithOwner
from utils.login import loggedIn
from DBModel.Key import Key as DBKey
from DBModel.Device import Device
from DBModel.db import psql_db

router = APIRouter(prefix="/api/key", tags=["key"])
@router.post("/", response_model=KeyWithOwner)
async def create_key(key: Key, device: Device = Depends(loggedIn)):
    """
    Create a key. 
    """

    @psql_db.atomic()
    def _create_key():
        db_key = DBKey.get_or_none(DBKey.name == key.name, DBKey.owner == device)
        if db_key is not None:
            raise HTTPException(status_code=400, detail="Key already exists")
        print(device.name)
        DBKey.create(name=key.name, pk=key.pk, owner=device)

    _create_key()
    return KeyWithOwner(name=key.name, pk=key.pk, owner=BaseDevice(name=device.name))

@router.get("/", response_model=list[KeyWithOwner])
async def get_keys(device = Depends(loggedIn)):
    """
    Get all keys for a device.
    """

    @psql_db.atomic()
    def _get_keys():
        res = DBKey.select().where(DBKey.owner == device)
        return res

    res = _get_keys()
    res = [KeyWithOwner(name=key.name, pk=key.pk, owner=BaseDevice(name=device.name)) for key in res]
    return res

@router.get("/{key_name}", response_model=KeyWithOwner)
async def get_key(key_name: str, device = Depends(loggedIn)):

    @psql_db.atomic()
    def _get_key():
        res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == device)
        if res is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return res
    res = _get_key()
    return KeyWithOwner(name=res.name, pk=res.pk, owner=BaseDevice(name=device.name))

@router.delete("/{key_name}")
async def delete_key(key_name: str, device = Depends(loggedIn)):

    @psql_db.atomic()
    def _delete_key():
        res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == device)
        if res is None:
            raise HTTPException(status_code=404, detail="Key not found")
        res.delete_instance()

    _delete_key()
    return {"message": "Deleted successfully"}

@router.put("/{key_name}", response_model=KeyWithOwner)
async def update_key(key_name: str, key: Key, device = Depends(loggedIn)):

    @psql_db.atomic()
    def _update_key():
        res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == device)
        if res is None:
            raise HTTPException(status_code=404, detail="Key not found")
        res.name = key.name
        res.pk = key.pk
        res.save()
        return res

    res = _update_key()
    return KeyWithOwner(name=res.name, pk=res.pk, owner=BaseDevice(name=device.name))
