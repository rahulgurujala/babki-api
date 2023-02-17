from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    account_name: str = Column(String, nullable=False)
    amount: float = Column(Float, nullable=False)
    is_debit: bool = Column(Boolean, nullable=False)
    category: str = Column(String, server_default="Other")
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    account_id: int = Column(Integer, ForeignKey("accounts.id"))

    def __init__(self, name, amount, is_debit) -> None:
        super().__init__()
        self.account_name = name
        self.amount = amount
        self.is_debit = is_debit

    def __repr__(self) -> str:
        return f"<Transaction {self.id}: {self.created_at}>"
