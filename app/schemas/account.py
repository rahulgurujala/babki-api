from pydantic import BaseModel


class AccountIn(BaseModel):
    account_type: str
    account_name: str
    balance: float
