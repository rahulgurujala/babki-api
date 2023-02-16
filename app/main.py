from fastapi import Depends, FastAPI, HTTPException, status
from models import *
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import engine, get_db

app = FastAPI()
