from enum import Enum

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class AccountIn(BaseModel):
    user_id: int
    account_type: str
    account_name: str
    balance: float


class TransactionType(str, Enum):
    credit = "CREDIT"
    debit = "DEBIT"


class TransactionIn(BaseModel):
    amount: str
    transaction_type: TransactionType
    # account: Account
