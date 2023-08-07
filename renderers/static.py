from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["static"])

@router.get("/public/{path}")
async def public(path: str):
    headers = {
            "Cache-Control": "public, max-age=31536000",
            }
    return FileResponse(f"public/{path}", headers=headers)

@router.get("/download/")
async def download():
    headers = {
            "Cache-Control": "public, max-age=31536000",
            }
    return FileResponse("public/cryptex.apk", headers=headers)
