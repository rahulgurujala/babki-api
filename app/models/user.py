from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.sql.expression import func, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from werkzeug.security import generate_password_hash

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, nullable=False)
    email: str = Column(String)
    password: str = Column(String, nullable=False)
    cash: float = Column(Float, server_default="0.0")
    savings: float = Column(Float, server_default="0.0")
    debt: float = Column(Float, server_default="0.0")
    loans: float = Column(Float, server_default="0.0")
    created_at: TIMESTAMP = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: TIMESTAMP = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    def __init__(self, email, password) -> None:
        super().__init__()
        # self.__dict__.update(kwargs)
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    @property
    def password(self):
        raise AttributeError("password is write-only")

    # Stores password in hashes
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
