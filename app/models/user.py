from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    accounts = relationship("Account", backref="user")
    transactions = relationship("Transaction", backref="user")

    def __repr__(self):
        return f"User {self.id}: {self.email}"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
