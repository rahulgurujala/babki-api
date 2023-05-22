from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.transaction import Category


class TransactionBase(BaseModel):
    user_id: int


class TransactionCreate(TransactionBase):
    amount: float
    is_debit: bool
    account_id: int


class TransactionUpdate(TransactionBase):
    amount: Optional[float]
    category: Optional[Category]


class Transaction(TransactionBase):
    id: int
    amount: float
    is_debit: bool
    account_id: int
    user_id: int
    category: Category
    created_at: datetime
    account_balance: Optional[float]

    class Config:
        orm_mode = True
