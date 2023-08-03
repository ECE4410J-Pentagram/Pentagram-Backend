from fastapi import FastAPI
from fastapi.responses import FileResponse
from renderers import login
from renderers import logout
from renderers import device
from renderers import key
from renderers import invitation
from renderers import friend
from fastapi.openapi.utils import get_openapi


app = FastAPI(openapi_url="/api/openapi.json", redoc_url="/api/docs")

app.include_router(login.loginRouter)
app.include_router(logout.router)

app.include_router(key.router)

app.include_router(device.router)
app.include_router(invitation.send_router)
app.include_router(invitation.receive_router)

app.include_router(friend.router)

@app.get("/api/public/{path}")
async def public(path: str):
    return FileResponse(f"public/{path}")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cryptex API",
        version="1.0",
        summary="Cryptex API for managing keys and devices",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/api/public/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
