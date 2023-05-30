from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.transaction import CategoryType


class TransactionBase(BaseModel):
    amount: float
    is_debit: bool
    account_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[CategoryType]


class Transaction(TransactionBase):
    id: int
    user_id: int
    category: CategoryType
    created_at: datetime
    account_balance: Optional[float]

    class Config:
        orm_mode = True
