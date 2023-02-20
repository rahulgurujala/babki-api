from pydantic import BaseModel


class AccountIn(BaseModel):
    user_id: int
    account_type: str
    account_name: str
    balance: float
