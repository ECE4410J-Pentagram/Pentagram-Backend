"""Login and token management"""
import secrets
from utils.models import Role
from fastapi import Header, HTTPException
from datetime import datetime
from DBModel.User import User
from DBModel.Device import select_device_by_user_name
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def random_token(length = 32):
    return secrets.token_urlsafe(length)

class TokenPayload(Role):
    login_time: float

def createToken(role: Role) -> str:
    # Create token
    payload = TokenPayload(login_time=datetime.now().timestamp(), user=role.user, device=role.device).json()
    print(payload)
    token = random_token()
    r.set(token, payload)
    # Set 30 days expiration
    r.expire(token, 60 * 60 * 24 * 30)
    return token

def loggedIn(Authorization: str = Header(...)):
    payload = r.get(Authorization)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    payload = TokenPayload.parse_raw(payload)
    
    username = payload.user.username
    device_name = payload.device.name
    db_user = User.get_or_none(username == username)

    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    db_device = select_device_by_user_name(db_user, device_name)
    if db_device is None:
        raise HTTPException(status_code=401, detail="Device not found")
    return db_user, db_device

def logout(Authorization: str = Header(...)):
    r.delete(Authorization)
