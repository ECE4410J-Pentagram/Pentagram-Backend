from fastapi import APIRouter, Depends, HTTPException, Header
from utils.login import loggedIn
from utils.models import BaseDevice, BaseKey
from DBModel.Key import Key
from DBModel.Device import Device
from DBModel.Relationship import Relationship
import pydantic
from typing import List

class PendingInvitation(pydantic.BaseModel):
    from_key: BaseKey
    to_device: BaseDevice

class PendingInvitationResponse(PendingInvitation):
    id: int
    from_key: BaseKey

class AcceptInvitationQuery(pydantic.BaseModel):
    id: int
    shared_key: BaseKey

class RejectInvitationQuery(pydantic.BaseModel):
    id: int


send_router = APIRouter(prefix="/api/invitation/sent", tags=["sending invitation"])

@send_router.post("/", response_model=PendingInvitationResponse)
async def send_invitation(invitiation: PendingInvitation, device: Device = Depends(loggedIn)):
    """
    Send an invitation to another device.
    """
    # Verifty that the key is valid
    key = Key.get_or_none(owner=device, name=invitiation.from_key.name)
    if key is None:
        raise HTTPException(status_code=404, detail="Key not found")

    # Verify that the device is valid
    to_device = Device.get_or_none(name=invitiation.to_device.name)
    if to_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    # Verify that the relationship does not already exist
    relationship = Relationship.get_or_none(to_device=to_device, from_key=key)
    if relationship is not None:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the relationship
    relationship = Relationship.create(from_key=key, from_device=device, to_device=to_device)

    return PendingInvitationResponse(from_key=BaseKey(name=key.name), to_device=BaseDevice(name=to_device.name), id = relationship.id)


@send_router.get("/", response_model=List[PendingInvitationResponse])
async def get_sent_invitations(device: Device = Depends(loggedIn)):
    """
    Get all sent invitations.
    """
    res = Relationship.select().join(Key, on=(Key.id==Relationship.from_key)).where(Key.owner == device, Relationship.pending == True)
    print(res)
    res = [PendingInvitationResponse(id = relationship.id, from_key=BaseKey(name=relationship.from_key.name), to_device=BaseDevice(name=relationship.to_device.name)) for relationship in res]
    return res


receive_router = APIRouter(prefix="/api/invitation/received", tags=["receiving invitation"])
@receive_router.get("/", response_model=List[PendingInvitationResponse])
async def get_received_invitations(device: Device = Depends(loggedIn)):
    """
    Get all received invitations.
    """
    res = Relationship.select().where(Relationship.to_device == device, Relationship.pending == True)
    res = [PendingInvitationResponse(id = relationship.id, from_key=BaseKey(name=relationship.from_key.name), to_device=BaseDevice(name=relationship.to_device.name)) for relationship in res]
    return res

@receive_router.post("/accept")
async def accept_invitation(accept: AcceptInvitationQuery, device: Device = Depends(loggedIn)):
    """
    Accept an invitation.
    """
    id = accept.id
    shared_key = accept.shared_key
    # Verifty that the key is valid
    shared_db_key = Key.get_or_none(owner=device, name=shared_key.name)
    if shared_db_key is None:
        raise HTTPException(status_code=404, detail="Key not found")

    # Verify that the relationship does not already exist
    try:
        relationship = Relationship.get_by_id(id)
    except Exception as _:
        raise HTTPException(status_code=404, detail="Relationship not found")
    if relationship.to_device != device:
        raise HTTPException(status_code=400, detail="Relationship does not exist")
    from_device = relationship.from_key.owner
    from_key = relationship.from_key
    to_device = relationship.to_device
    to_key = shared_db_key

    # Verify that no such relationship already exists
    relationship = Relationship.get_or_none(from_key=from_key, to_device=to_device, pending = False)
    if relationship is not None:
        raise HTTPException(status_code=400, detail="Relationship already exists")
    relationship = Relationship.get_or_none(from_key=to_key, to_device=from_device, pending = False)
    if relationship is not None:
        raise HTTPException(status_code=400, detail="Relationship already exists")
    # Accept the relationship
    relationship = Relationship.get_by_id(id)
    relationship.pending = False
    relationship.to_key = to_key
    relationship.save()

    return PendingInvitation(from_key=BaseKey(name = relationship.from_key.name), to_device=BaseDevice(name = relationship.to_device.name))

@receive_router.post("/reject")
async def reject_invitation(reject: RejectInvitationQuery, device: Device = Depends(loggedIn)):
    """
    Reject an invitation.
    """
    id = reject.id
    # Verify that the relationship does not already exist
    relationship = Relationship.get_by_id(id)
    if relationship.to_device != device:
        raise HTTPException(status_code=400, detail="Relationship does not exist")
    # Accept the relationship
    res = PendingInvitation(from_key=BaseKey(name = relationship.from_key.name), to_device=BaseDevice(name = relationship.to_device.name))
    relationship.delete_instance()

    return res
