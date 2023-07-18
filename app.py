from fastapi import FastAPI
from renderers import user
from renderers import key

app = FastAPI()
app.include_router(user.router)
app.include_router(user.loginRouter)
app.include_router(user.logoutRouter)

app.include_router(key.router)
