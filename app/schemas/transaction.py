from enum import Enum

from pydantic import BaseModel

from .account import Account


class TransactionType(str, Enum):
    credit = "CREDIT"
    debit = "DEBIT"


class TransactionBase(BaseModel):
    amount: str
    transaction_type: TransactionType


class TransactionCreate(TransactionBase):
    account_number: str


class Transaction(BaseModel):
    account: Account
