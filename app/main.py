from fastapi import FastAPI

from app.routers import account, auth, user

app = FastAPI()

app.include_router(user.router)
app.include_router(account.router)
app.include_router(auth.router)
