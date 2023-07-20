from fastapi import FastAPI
from renderers import login
from renderers import logout
from renderers import device
from renderers import key
from renderers import invitation
from renderers import friend

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")

app.include_router(login.loginRouter)
app.include_router(logout.router)

app.include_router(key.router)

app.include_router(device.router)
app.include_router(invitation.send_router)
app.include_router(invitation.receive_router)

app.include_router(friend.router)
