from fastapi import APIRouter, Depends, HTTPException
from utils.login import loggedIn
from utils.models import BaseUser
import pydantic
from DBModel.Key import Key as DBKey

class Key(pydantic.BaseModel):
    name: str = pydantic.Field(min_length=10, max_length=1024)
    pk: str = pydantic.Field(max_length=2048)

class KeyWithOwner(Key):
    owner: BaseUser

router = APIRouter(prefix="/api/key", tags=["key"])
@router.post("/", response_model=KeyWithOwner)
async def create_key(key: Key, role = Depends(loggedIn)):
    user, device = role
    if DBKey.select().where(DBKey.name == key.name, DBKey.owner == user, DBKey.device == device).exists():
        raise HTTPException(status_code=400, detail="Key already exists")
    DBKey.create(name=key.name, pk=key.pk, owner=user, device=device)
    return KeyWithOwner(name=key.name, pk=key.pk, owner=BaseUser(username=user.username))

@router.get("/", response_model=list[KeyWithOwner])
async def get_keys(role = Depends(loggedIn)):
    user, device = role
    res = DBKey.select().where(DBKey.owner == user, DBKey.device == device)
    res = [KeyWithOwner(name=key.name, pk=key.pk, owner=BaseUser(username=user.username)) for key in res]
    return res

@router.get("/{key_name}", response_model=KeyWithOwner)
async def get_key(key_name: str, role = Depends(loggedIn)):
    user, device = role
    res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == user, DBKey.device == device)
    if res is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return KeyWithOwner(name=res.name, pk=res.pk, owner=BaseUser(username=user.username))

@router.delete("/{key_name}")
async def delete_key(key_name: str, role = Depends(loggedIn)):
    user, device = role
    res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == user, DBKey.device == device)
    if res is None:
        raise HTTPException(status_code=404, detail="Key not found")
    res.delete_instance()
    return {"message": "Deleted successfully"}

@router.put("/{key_name}", response_model=KeyWithOwner)
async def update_key(key_name: str, key: Key, role = Depends(loggedIn)):
    user, device = role
    res = DBKey.get_or_none(DBKey.name == key_name, DBKey.owner == user, DBKey.device == device)
    if res is None:
        raise HTTPException(status_code=404, detail="Key not found")
    res.name = key.name
    res.pk = key.pk
    res.save()
    return KeyWithOwner(name=res.name, pk=res.pk, owner=BaseUser(username=user.username))
