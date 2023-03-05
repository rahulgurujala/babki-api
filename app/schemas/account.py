from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccountBase(BaseModel):
    account_type: str
    account_name: str
    account_number: Optional[str]
    balance: float
    currency: Optional[str]


class AccountCreate(AccountBase):
    user_id: int


class Account(AccountBase):
    user_id: int
    id: int
    created_at: datetime
    updated_at: datetime = None

    class Config:
        orm_mode = True


class AccountUpdate(BaseModel):
    account_name: Optional[str]
    balance: Optional[float]
