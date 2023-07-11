import pydantic
class BaseUser(pydantic.BaseModel):
    username: str = pydantic.Field(..., min_length=3, max_length=20)

class LoginHeader(pydantic.BaseModel):
    Authorization: str = pydantic.Field(..., min_length=1)
