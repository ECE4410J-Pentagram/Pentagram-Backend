from fastapi import FastAPI
from renderers import user

app = FastAPI()
app.include_router(user.router)
app.include_router(user.loginRouter)
app.include_router(user.logoutRouter)

