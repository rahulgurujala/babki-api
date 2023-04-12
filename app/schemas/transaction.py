from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.transaction import Category


class TransactionBase(BaseModel):
    amount: float
    transaction_type: bool
    created_at: datetime = None


class TransactionCreate(TransactionBase):
    user_id: int
    account_id: int


class TransactionUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[Category]
    transaction_type: bool


class Transaction(TransactionBase):
    id: int
    account_id: int
    user_id: int
    category: Category

    class Config:
        orm_mode = True
