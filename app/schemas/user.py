from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from .account import Account


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdateIn(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]


class UserUpdateOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime = None
    accounts: list[Account]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
