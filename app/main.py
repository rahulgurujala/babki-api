from fastapi import FastAPI

from app.routers import account, auth, transaction, user

app = FastAPI()

app.include_router(user.router)
app.include_router(account.router)
app.include_router(auth.router)
app.include_router(transaction.router)
