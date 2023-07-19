from fastapi import APIRouter, HTTPException, Request, Depends, Header
from DBModel.User import User, hash_password, check_password
from DBModel.Device import Device
from utils.models import BaseUser, BaseDevice, Role
from utils.login import loggedIn, createToken
from utils.login import logout as logout_func
import utils.message as message

class RegisterUser(BaseUser):
    password: str

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/", response_model=BaseUser)
async def create_user(user: RegisterUser):
    prev_user = User.select().where(User.username == user.username)
    if prev_user.exists():
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User.create(username=user.username, hashed_password=hash_password(user.password))
    print(new_user)
    return BaseUser(username=new_user.username)
    
@router.get("/", response_model=BaseUser)
async def get_me(role: tuple[User, Device] = Depends(loggedIn)):
    user, _ = role
    return BaseUser(username=user.username)

logoutRouter = APIRouter(prefix="/api/logout", tags=["logout"])
@logoutRouter.post("/", response_model=message.Message)
async def logout(Authorization: str = Header(...), _: tuple[User, Device] = Depends(loggedIn)):
    logout_func(Authorization)
    return message.Message("Logout successfully")
