from fastapi import FastAPI
from renderers import login
from renderers import logout
from renderers import device
from renderers import key

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")

app.include_router(login.loginRouter)
app.include_router(logout.router)

app.include_router(key.router)

app.include_router(device.router)
