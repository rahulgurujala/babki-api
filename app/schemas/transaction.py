from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.transaction import Category


class TransactionBase(BaseModel):
    amount: float
    is_debit: bool


class TransactionCreate(TransactionBase):
    user_id: int
    account_id: int


class TransactionUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[Category]


class Transaction(TransactionBase):
    id: int
    account_id: int
    user_id: int
    category: Category
    created_at: datetime

    class Config:
        orm_mode = True
