import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class CurrencyType(str, enum.Enum):
    RUB = "RUB"
    USD = "USD"


class AccountType(str, enum.Enum):
    CASH = "Cash"
    DEBIT_CREDIT_CARD = "Debit/Credit Card"
    CHECKING = "Checking"
    DEPOSIT = "Deposit"
    LOAN = "Loan"


class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    account_type: str = Column(Enum(AccountType, name="account_type"), nullable=False)
    account_name: str = Column(String(50), nullable=False)
    balance: float = Column(Float, server_default="0.0")
    currency: str = Column(
        Enum(CurrencyType, name="currency_type"), server_default="RUB"
    )
    account_number: str = Column(String(20))
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: TIMESTAMP = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    transactions = relationship("Transaction", backref="account")
