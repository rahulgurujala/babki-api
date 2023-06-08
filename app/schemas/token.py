from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    expires_in: int


class TokenData(BaseModel):
    id: int
