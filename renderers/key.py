from fastapi import APIRouter, Depends
from utils.login import BaseUser, loggedIn
import pydantic

class Key(pydantic.BaseModel):
    name: str
    pk: str

class KeyWithOwner(Key):
    owner: BaseUser

router = APIRouter(prefix="/key", tags=["key"])
@router.post("/")
async def create_key(key: Key, user = Depends(loggedIn)):
    pass

