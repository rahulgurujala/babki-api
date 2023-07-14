from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.models.transaction import CategoryType

from .account import Account


class TransactionBase(BaseModel):
    amount: float
    is_debit: bool
    account_id: int


class TransactionCreate(TransactionBase):
    category: Optional[CategoryType]


class TransactionUpdate(BaseModel):
    amount: Optional[float]
    is_debit: bool
    category: Optional[CategoryType]


class Transaction(TransactionBase):
    id: int
    user_id: int
    category: CategoryType
    created_at: datetime
    account_balance: float = Field(..., alias="account")

    @validator("account_balance", pre=True)
    def set_account_balance(cls, value):
        print(value)
        return value.balance

    class Config:
        orm_mode = True
