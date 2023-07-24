from fastapi import APIRouter, Depends, HTTPException, Header
from utils.login import loggedIn
from DBModel.Device import Device
from DBModel.Relationship import Relationship
from DBModel.Key import Key
from utils.models import BaseDevice, InfoDevice, KeyWithOwner
from utils.device import infodevice
from typing import List
from DBModel.db import psql_db

router = APIRouter(prefix="/api/friend", tags=["friend"])

def get_Baseowner(owner):
    return BaseDevice(name = owner.name)

@psql_db.atomic()
def query_friends(device: Device):
    from_key = Key.select().join(Relationship, on = (Relationship.to_key == Key.id)).where(Relationship.from_device == device)
    from_key = [KeyWithOwner(name = key.name, pk = key.pk, owner = get_Baseowner(key.owner)) for key in from_key]

    to_key = Key.select().join(Relationship, on = (Relationship.from_key == Key.id)).where(Relationship.to_device == device)
    to_key = [KeyWithOwner(name = key.name, pk = key.pk, owner = get_Baseowner(key.owner)) for key in to_key]

    return from_key + to_key

@router.get("/", response_model=List[KeyWithOwner])
async def get_friends(device = Depends(loggedIn)):
    db_friends = query_friends(device)
    print(db_friends)
    print(type(db_friends))
    return db_friends
