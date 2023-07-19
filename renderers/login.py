from fastapi import APIRouter, HTTPException
from utils.models import BaseUser, BaseDevice, Role
from utils.login import createToken, random_token
import pydantic
from DBModel.User import User, check_password
from DBModel.Device import Device, Owener_Device_Relationship

class LoginUser(BaseUser):
    password: str

class LoginDevice(pydantic.BaseModel):
    name: str
    key: str | None

class LoginRole(pydantic.BaseModel):
    user: LoginUser
    device: LoginDevice

class TokenResponse(pydantic.BaseModel):
    Authorization: str

loginRouter = APIRouter(prefix="/api/login", tags=["login"])
@loginRouter.post("/", response_model=TokenResponse)
async def login(role: LoginRole):
    user = role.user
    device = role.device
    db_user = User.get_or_none(User.username == user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username does not exist")
    if not check_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password is incorrect")

    if device.key is None:
        device.key = random_token()
        new_db_device = Device.create(name=device.name, key=device.key)
        Owener_Device_Relationship.create(device=new_db_device, user=db_user)
    
    db_device = Device.select(Device, Owener_Device_Relationship).join(Owener_Device_Relationship).where(Device.name == device.name, Device.key == device.key, Owener_Device_Relationship.user == db_user).first()
    print(db_device)

    output_user = BaseUser(username=db_user.username)
    output_device = BaseDevice(name=db_device.name, key=db_device.key)
    output_role = Role(user=output_user, device=output_device)



    return TokenResponse(Authorization=createToken(output_role))

