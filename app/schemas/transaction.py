from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.transaction import Category, TransactionType


class TransactionBase(BaseModel):
    amount: float
    transaction_type: TransactionType
    created_at: datetime = None


class TransactionCreate(TransactionBase):
    account_id: int


class TransactionUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[Category]
    transaction_type: Optional[TransactionType]


class Transaction(TransactionBase):
    id: int
    account_id: int
    category: Category

    class Config:
        orm_mode = True
