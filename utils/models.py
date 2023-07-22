import pydantic
class BaseDevice(pydantic.BaseModel):
    name: str = pydantic.Field(..., min_length=1, max_length=1024)

class LoginDevice(BaseDevice):
    key: str

class LoginHeader(pydantic.BaseModel):
    Authorization: str = pydantic.Field(..., min_length=1)

class BaseKey(pydantic.BaseModel):
    name: str = pydantic.Field(min_length=10, max_length=1024)

class Key(BaseKey):
    pk: str = pydantic.Field(max_length=2048)

class InfoDevice(BaseDevice):
    keys: list[Key]

class KeyWithOwner(Key):
    owner: BaseDevice

