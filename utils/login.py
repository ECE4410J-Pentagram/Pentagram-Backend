"""Login and token management"""
import secrets
from utils.models import BaseDevice, LoginDevice
from fastapi import Header, HTTPException
from datetime import datetime
from DBModel.Device import Device
from config import config
import redis

r = redis.Redis(host=config.REDIS_HOST, port=6379, decode_responses=True)

def random_token(length = 32):
    return secrets.token_urlsafe(length)

class TokenPayload(LoginDevice):
    login_time: float

def createToken(device: LoginDevice) -> str:
    # Create token
    payload = TokenPayload(login_time=datetime.now().timestamp(), name = device.name, key=device.key).json()
    print(payload)
    token = random_token()
    r.set(token, payload)
    # Set 30 days expiration
    r.expire(token, 60 * 60 * 24 * 30)
    return token

def loggedIn(Authorization: str = Header(...)) -> Device:
    payload = r.get(Authorization)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    payload = TokenPayload.parse_raw(payload)
    
    db_device = Device.get_or_none(Device.name == payload.name, Device.key == payload.key)
    if db_device is None:
        raise HTTPException(status_code=401, detail="Device not found")
    return db_device

def logout(Authorization: str = Header(...)):
    res = loggedIn(Authorization)
    r.delete(Authorization)
    return res
