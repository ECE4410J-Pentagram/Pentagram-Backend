from fastapi import APIRouter, Depends, HTTPException, Header
from utils.login import loggedIn
from DBModel.Device import Device
from DBModel.Relationship import Relationship
from DBModel.Key import Key
from utils.models import BaseDevice, DummyMessage, KeyWithOwner
from utils.device import infodevice
from typing import List
from DBModel.db import psql_db
import pydantic

router = APIRouter(prefix="/api/friend", tags=["friend"])

def get_Baseowner(owner):
    return BaseDevice(name = owner.name)

class FriendRequest(pydantic.BaseModel):
    id: int

class FriendInfo(KeyWithOwner):
    id: int

@psql_db.atomic()
def query_friends(device: Device):
    from_relationship = Relationship.select().where(Relationship.from_device == device, Relationship.pending == False)
    from_key = [FriendInfo(
        name = relationship.to_key.name, 
        pk = relationship.to_key.pk, 
        owner = get_Baseowner(relationship.to_key.owner),
        id = relationship.id) for relationship in from_relationship]

    to_relationship = Relationship.select().where(Relationship.to_device == device, Relationship.pending == False)
    to_key = [FriendInfo(
        name = relationship.from_key.name,
        pk = relationship.from_key.pk,
        owner = get_Baseowner(relationship.from_key.owner),
        id = relationship.id) for relationship in to_relationship]

    # from_key = Key.select().join(Relationship, on = (Relationship.to_key == Key.id)).where(Relationship.from_device == device, Relationship.pending == False)
    # from_key = [KeyWithOwner(name = key.name, pk = key.pk, owner = get_Baseowner(key.owner)) for key in from_key]

    # to_key = Key.select().join(Relationship, on = (Relationship.from_key == Key.id)).where(Relationship.to_device == device, Relationship.pending == False)
    # to_key = [KeyWithOwner(name = key.name, pk = key.pk, owner = get_Baseowner(key.owner)) for key in to_key]

    return from_key + to_key

@router.get("/", response_model=List[FriendInfo])
async def get_friends(device = Depends(loggedIn)):
    db_friends = query_friends(device)
    print(db_friends)
    print(type(db_friends))
    return db_friends

@router.delete("/", response_model=DummyMessage)
async def delete_friend(friendship: FriendRequest, device: Device = Depends(loggedIn)):
    """
    Delete a friend
    """

    @psql_db.atomic()
    def _delete_friend():
        try:
            relationship = Relationship.get_by_id(friendship.id)
        except Exception as e:
            raise HTTPException(status_code=404, detail="Relationship not found")
        if relationship.from_device != device and relationship.to_device != device:
            raise HTTPException(status_code=403, detail="You are not part of this relationship")
        relationship.delete_instance()

    _delete_friend()
    return {"message": "Relationship deleted"}

