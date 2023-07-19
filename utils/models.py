import pydantic
class BaseUser(pydantic.BaseModel):
    username: str = pydantic.Field(..., min_length=3, max_length=20)

class BaseDevice(pydantic.BaseModel):
    device_id: str = pydantic.Field(..., min_length=1, max_length=64)

class Role(pydantic.BaseModel):
    user: BaseUser
    device: BaseDevice

class LoginHeader(pydantic.BaseModel):
    Authorization: str = pydantic.Field(..., min_length=1)
