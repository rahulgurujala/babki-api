from datetime import datetime
from enum import Enum
from typing import Optional

from click import option
from pydantic import BaseModel

from .account import Account


class TransactionType(str, Enum):
    credit = "CREDIT"
    debit = "DEBIT"


class TransactionBase(BaseModel):
    amount: float
    transaction_type: TransactionType
    created_at: datetime = None


class TransactionCreate(TransactionBase):
    account_id: int


class Transaction(TransactionBase):
    account_id: int

    class Config:
        orm_mode = True
