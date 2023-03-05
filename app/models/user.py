from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from werkzeug.security import generate_password_hash

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    cash: float = Column(Float, server_default="0.0")
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: TIMESTAMP = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    accounts = relationship("Account", backref="owner")

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"
