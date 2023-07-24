from fastapi import APIRouter, HTTPException, Depends
from utils.models import BaseDevice, LoginDevice
from utils.login import createToken, check_key
import pydantic
from DBModel.Device import Device
from utils.peewee import get_db
from DBModel.db import psql_db

class TokenResponse(pydantic.BaseModel):
    Authorization: str

loginRouter = APIRouter(prefix="/api/login", tags=["login"])
@loginRouter.post("/", response_model=TokenResponse)
async def login(device: LoginDevice, db = Depends(get_db)):

    @psql_db.atomic()
    def _login():
        db_device = Device.get_or_none(Device.name == device.name)
        return db_device

    db_device = _login()
    if db_device == None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not check_key(device.key, db_device.key_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(Authorization=createToken(device))

