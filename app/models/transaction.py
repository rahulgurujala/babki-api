import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class TransactionType(str, enum.Enum):
    CREDIT = "Credit"
    DEBIT = "Debit"


class Category(str, enum.Enum):
    HEALTH = "Health"
    FOOD = "Food"
    GROCERIES = "Groceries"
    TRANSFER = "Transfer"
    TRANSPORT = "Transport"
    TRAVEL = "Travel"
    WITHDRAW = "Withdraw"
    OTHERS = "Others"
    SUBSCRIPTIONS = "Subscriptions"


class Transaction(Base):
    __tablename__ = "transactions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    amount: float = Column(Float, nullable=False)
    transaction_type: bool = Column(
        Enum(TransactionType, name="transaction_type"),
        nullable=False,
    )
    category: str = Column(Enum(Category, name="category"))
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    account_id: int = Column(
        Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )
    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
