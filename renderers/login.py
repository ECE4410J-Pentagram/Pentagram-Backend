from fastapi import APIRouter, HTTPException
from utils.login import BaseUser, createToken
import pydantic
from DBModel.User import User, check_password

class LoginUser(BaseUser):
    password: str
    device_id: str

class TokenResponse(pydantic.BaseModel):
    Authorization: str

loginRouter = APIRouter(prefix="/api/login", tags=["login"])
@loginRouter.post("/", response_model=TokenResponse)
async def login(user: LoginUser):
    prev_user = User.get_or_none(User.username == user.username)
    print(prev_user)
    if prev_user is None:
        raise HTTPException(status_code=400, detail="Username does not exist")
    if not check_password(user.password, prev_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password is incorrect")
    return TokenResponse(Authorization=createToken(BaseUser(username=prev_user.username)))

