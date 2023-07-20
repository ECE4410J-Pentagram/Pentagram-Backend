import pydantic
class BaseDevice(pydantic.BaseModel):
    name: str = pydantic.Field(..., min_length=1, max_length=1024)

class LoginDevice(BaseDevice):
    key: str

class LoginHeader(pydantic.BaseModel):
    Authorization: str = pydantic.Field(..., min_length=1)
