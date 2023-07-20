from fastapi import APIRouter, HTTPException
from utils.models import BaseDevice, LoginDevice
from utils.login import createToken, random_token
import pydantic
from DBModel.Device import Device

class TokenResponse(pydantic.BaseModel):
    Authorization: str

loginRouter = APIRouter(prefix="/api/login", tags=["login"])
@loginRouter.post("/", response_model=TokenResponse)
async def login(device: LoginDevice):
    db_device = Device.get_or_none(Device.key == device.key, Device.name == device.name)
    if db_device == None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(Authorization=createToken(device))

