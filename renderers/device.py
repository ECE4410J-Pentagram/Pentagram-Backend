from fastapi import APIRouter, Depends, HTTPException, Header
from DBModel.Device import Device 
from utils.models import BaseDevice
from utils.login import loggedIn, logout
from .login import LoginDevice

router = APIRouter(prefix="/api/device", tags=["device"])

class InfoDevice(BaseDevice):
    pass



@router.get("/", response_model=InfoDevice)
async def get_device(device: Device = Depends(loggedIn)):
    return InfoDevice(name=device.name)

@router.post("/", response_model=InfoDevice)
async def create_device(device: LoginDevice):
    """
    Create a device. 
    """
    device = Device.create(name=device.name, key=device.key)
    return InfoDevice(name=device.name)

@router.put("/", response_model=InfoDevice)
async def update_device(device: BaseDevice, credential: Device = Depends(loggedIn)):
    """
    Update a device. 
    """
    credential.name = device.name
    credential.save()
    return InfoDevice(name=device.name)


@router.delete("/", response_model=InfoDevice)
async def delete_device(device: Device = Depends(logout)):
    """
    Delete a device. 
    Note you probably want to log out if you delete the device you are currently using.
    """
    device.delete_instance()
    return InfoDevice(name=device.name)
