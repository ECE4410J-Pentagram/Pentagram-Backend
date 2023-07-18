"""Login and token management"""
import secrets
from utils.models import BaseUser
from config import config
from fastapi import Header, HTTPException
from datetime import datetime
from pydantic import BaseModel
from DBModel.User import User
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def random_token():
    return secrets.token_urlsafe(32)

class TokenPayload(BaseUser):
    login_time: float

def createToken(user: BaseUser) -> str:
    payload = TokenPayload(login_time=datetime.now().timestamp(), username=user.username).json()
    print(payload)
    token = random_token()
    r.set(token, payload)
    return token

def loggedIn(Authorization: str = Header(...)):
    payload = r.get(Authorization)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    payload = TokenPayload.parse_raw(payload)
    
    username = payload.username
    user = User.get_or_none(username == username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return BaseUser(username=user.username)

def logout(Authorization: str = Header(...)):
    r.delete(Authorization)
