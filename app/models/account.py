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

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_type = Column(Enum(AccountType, name="account_type"), nullable=False)
    account_name = Column(String(), nullable=False)
    balance = Column(Float, server_default="0.0")
    currency = Column(Enum(CurrencyType, name="currency_type"), server_default="RUB")
    account_number = Column(String())
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    transactions = relationship("Transaction", backref="account")

    def __repr__(self):
        return f"Account {self.id}: {self.account_name}"

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
