from fastapi import APIRouter, Depends, HTTPException, Header
from DBModel.Device import Device 
from utils.models import BaseDevice, InfoDevice
from utils.login import loggedIn, logout
from utils.device import infodevice
from .login import LoginDevice

router = APIRouter(prefix="/api/device", tags=["device"])



@router.get("/", response_model=InfoDevice)
async def get_device(device: Device = Depends(loggedIn)):
    return infodevice(device.name)

@router.post("/", response_model=InfoDevice)
async def create_device(device: LoginDevice):
    """
    Create a device. 
    """
    # Verify if the device already exists
    db_device = Device.get_or_none(name=device.name)
    if db_device:
        raise HTTPException(status_code=400, detail="Device already exists")
    db_device = Device.create(name=device.name, key=device.key)
    return infodevice(device.name)

@router.put("/", response_model=InfoDevice)
async def update_device(device: BaseDevice, credential: Device = Depends(loggedIn)):
    """
    Update a device. 
    """
    credential.name = device.name
    credential.save()
    return infodevice(credential.name)


@router.delete("/", response_model=InfoDevice)
async def delete_device(device: Device = Depends(logout)):
    """
    Delete a device. 
    Note you probably want to log out if you delete the device you are currently using.
    """
    res = infodevice(device.name)
    device.delete_instance()
    return res
