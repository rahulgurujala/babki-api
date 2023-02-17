from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    account_type: str = Column(String, nullable=False)
    account_name: str = Column(String(50))
    bank_name: str = Column(String)
    amount: float = Column(Float, server_default="0.0")
    currency: str = Column(String, server_default="RUB")
    account_number: str = Column(String(20))
    user_id: int = Column(Integer, ForeignKey("users.id"))
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: TIMESTAMP = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    def __init__(self, account_type) -> None:
        super().__init__()
        self.account_type = account_type

    def __repr__(self) -> str:
        return f"<Account {self.id}: {self.created_at}>"
