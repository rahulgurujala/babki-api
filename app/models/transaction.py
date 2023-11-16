import enum

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class CategoryType(str, enum.Enum):
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    is_debit = Column(Boolean, nullable=False)
    category = Column(Enum(CategoryType, name="category_type"), server_default="OTHERS")
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    account = relationship("Account", back_populates="account")
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="user")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
