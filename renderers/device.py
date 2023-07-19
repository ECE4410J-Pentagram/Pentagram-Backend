from fastapi import APIRouter, Depends, HTTPException, Header
from DBModel.Device import select_all_devices_by_user, Device, select_device_by_user_name
from DBModel.User import User
from utils.models import BaseDevice
from utils.login import loggedIn, logout

router = APIRouter(prefix="/api/device", tags=["key"])

class InfoDevice(BaseDevice):
    pass

@router.get("/", response_model=list[InfoDevice])
async def get_devices(role: tuple[User, Device] = Depends(loggedIn)):
    user, _ = role
    devices = select_all_devices_by_user(user)
    return [InfoDevice(name=device.name) for device in devices]

@router.delete("/{device_name}")
async def delete_device(device_name: str, role: tuple[User, Device] = Depends(loggedIn), Authorization: str = Header(...)):
    """
    Delete a device. 
    Note you probably want to log out if you delete the device you are currently using.
    """
    user, device = role
    device = select_device_by_user_name(user, device_name)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    device.delete_instance()
    if device.name == device_name:
        logout(Authorization)

    return {"message": "Deleted successfully"}
