from fastapi import APIRouter, Depends, HTTPException, Header
from utils.login import loggedIn
from DBModel.Device import Device
from DBModel.Relationship import Relationship
from DBModel.Key import Key
from utils.models import BaseDevice, InfoDevice, KeyWithOwner
from utils.device import infodevice
from typing import List

router = APIRouter(prefix="/api/friend", tags=["friend"])

def get_Baseowner(owner):
    return BaseDevice(name = owner.name)

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

@router.delete("/")
async def delete_friend(friend_key: KeyWithOwner, device: Device = Depends(loggedIn)):
    """
    Delete a friend
    """
    # Verify that the device is valid
    friend_device = Device.get_or_none(name=friend_key.owner.name)
    if friend_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    # Verify that the relationship exists
    relationship = Relationship.get_or_none(from_device=device, to_device=friend_device, to_key=friend_key.name)
    if relationship is None:
        relationship = Relationship.get_or_none(from_device=friend_device, to_device=device, from_key=friend_key.name)
        if relationship is None:
            raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the relationship
    relationship.delete_instance()
    return {"detail": "Relationship deleted"}

