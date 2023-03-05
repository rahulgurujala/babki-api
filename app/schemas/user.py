from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from .account import Account


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    cash: Optional[float]


class User(UserBase):
    id: int
    cash: float
    created_at: datetime
    updated_at: datetime = None
    accounts: list[Account]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
