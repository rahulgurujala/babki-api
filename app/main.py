from fastapi import FastAPI

from app.routers import account, user

app = FastAPI()

app.include_router(user.router)
app.include_router(account.router)
