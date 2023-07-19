from fastapi import APIRouter, HTTPException, Request, Depends, Header
from DBModel.User import User, hash_password, check_password
from utils.models import BaseUser
from utils.login import loggedIn, createToken
from utils.login import logout as logout_func
import pydantic

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
async def get_me(user: User = Depends(loggedIn)):
    return BaseUser(username=user.username)

logoutRouter = APIRouter(prefix="/api/logout", tags=["logout"])
@logoutRouter.post("/")
async def logout(Authorization: str = Header(...)):
    logout_func(Authorization)
    return {"message": "Logged out successfully"}
