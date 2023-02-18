from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from . import models
from .database import get_db
from .routers import user
from .schemas import *

app = FastAPI()

app.include_router(user.router)
