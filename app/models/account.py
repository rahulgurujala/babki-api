from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    account_type: str = Column(String, nullable=False)
    account_name: str = Column(String(50), nullable=False)
    balance: float = Column(Float, server_default="0.0")
    currency: str = Column(String, server_default="RUB")
    account_number: str = Column(String(20))
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    user_id: int = Column(Integer, ForeignKey("users.id"))
    updated_at: TIMESTAMP = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    transactions = relationship("Transaction", backref="account")

    def __repr__(self) -> str:
        return f"<Account {self.id}: {self.created_at}>"
