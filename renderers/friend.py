from fastapi import APIRouter, Depends, HTTPException, Header
from utils.login import loggedIn
from DBModel.Device import Device
from DBModel.Relationship import Relationship
from utils.models import BaseDevice, InfoDevice
from utils.device import infodevice

router = APIRouter(prefix="/api/friend", tags=["friend"])

def query_friends(device: Device):
    from_friends = Relationship.select().join(Device, on=(Device.id==Relationship.from_key.owner)).where(Device.id == device.id, Relationship.pending == False)

    to_friends = Relationship.select().join(Device, on=(Device.id==Relationship.to_device)).where(Device.id == device.id, Relationship.pending == False)

    friends = {}
    for friend in from_friends:
        friends[friend.to_device.key] = friend.to_device

    for friend in to_friends:
        friends[friend.from_key.key.owner.key] = friend.from_key.owner

    friends = list(friends.values())
    return friends

@router.get("/", response_model=list[InfoDevice])
async def get_friends(device = Depends(loggedIn)):
    db_friends = query_friends(device)
    friends = [infodevice(key = friend.key) for friend in db_friends]
    return friends
