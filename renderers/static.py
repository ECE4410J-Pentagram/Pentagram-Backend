from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["static"])

@router.get("/public/{path}")
async def public(path: str):
    return FileResponse(f"public/{path}")

@router.get("/download/")
async def download():
    return FileResponse("public/cryptex.apk")
