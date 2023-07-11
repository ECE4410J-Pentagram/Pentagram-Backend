import jwt
from utils.models import BaseUser
from config import config
from fastapi import Header, HTTPException
from datetime import datetime
from pydantic import BaseModel

class Token(BaseModel):
    login_time: float
    user: BaseUser

def createToken(user: BaseUser) -> str:
    payload = Token(login_time=datetime.now().timestamp(), user=user).dict()
    print(payload)
    encoded = jwt.encode(payload, config.JWT_SECRET, algorithm='HS256')
    return encoded

def loggedIn(Authorization: str = Header(...)):
    try:
        token = jwt.decode(Authorization, config.JWT_SECRET, algorithms=['HS256'])
        token = Token(**token)
        return token.user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
