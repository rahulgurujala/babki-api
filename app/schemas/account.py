from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from ..models.account import AccountType


class AccountBase(BaseModel):
    account_name: str
    account_number: Optional[str]
    account_type: AccountType
    balance: float
    currency: Optional[str]

    @validator("balance")
    def set_decimal_places(cls, value):
        return round(value, 2)


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime = None
    user_id: int

    class Config:
        orm_mode = True


class AccountUpdate(BaseModel):
    account_name: Optional[str]
    account_number: Optional[str]
    account_type: Optional[AccountType]
    balance: Optional[float]
    currency: Optional[str]
