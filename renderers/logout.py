from fastapi import APIRouter, Header, Depends
from utils.login import logout as logout_func, loggedIn
from DBModel.Device import Device

router = APIRouter(prefix="/api/logout", tags=["logout"])
@router.post("/")
async def logout(device : Device = Depends(logout_func)):
    return {"message": "Logged out"}

