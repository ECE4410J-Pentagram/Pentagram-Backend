from fastapi import APIRouter, HTTPException, Request, Depends, Header
from DBModel.User import User, hash_password, check_password
from utils.models import BaseUser
from utils.login import loggedIn, createToken
from utils.login import logout as logout_func
import pydantic

class RegisterUser(BaseUser):
    password: str
    public_key: str

class LoginUser(BaseUser):
    password: str

class TokenResponse(pydantic.BaseModel):
    Authorization: str

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=BaseUser)
async def create_user(user: RegisterUser):
    prev_user = User.select().where(User.username == user.username)
    if prev_user.exists():
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User.create(username=user.username, hashed_password=hash_password(user.password))
    return BaseUser(username=new_user.username)
    
@router.get("/", response_model=BaseUser)
async def get_me(user: User = Depends(loggedIn)):
    return BaseUser(username=user.username)

loginRouter = APIRouter(prefix="/login", tags=["login"])
@loginRouter.post("/", response_model=TokenResponse)
async def login(user: LoginUser):
    prev_user = User.get_or_none(User.username == user.username)
    print(prev_user)
    if prev_user is None:
        raise HTTPException(status_code=400, detail="Username does not exist")
    if not check_password(user.password, prev_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password is incorrect")
    return TokenResponse(Authorization=createToken(BaseUser(username=prev_user.username)))

logoutRouter = APIRouter(prefix="/logout", tags=["logout"])
@logoutRouter.post("/")
async def logout(Authorization: str = Header(...)):
    logout_func(Authorization)
    return {"message": "Logged out successfully"}
