from fastapi import APIRouter, Header, Depends
from utils.login import logout as logout_func, loggedIn
from utils.models import DummyMessage
from DBModel.Device import Device

router = APIRouter(prefix="/api/logout", tags=["logout"])
@router.post("/", response_model=DummyMessage)
async def logout(device : Device = Depends(logout_func)):
    return {"message": "Logged out"}

