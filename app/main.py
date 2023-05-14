from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import account, auth, transaction, user

app = FastAPI(docs_url="/", title="denarii API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(account.router)
app.include_router(auth.router)
app.include_router(transaction.router)
