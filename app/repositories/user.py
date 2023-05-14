from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserUpdateIn
from app.schemas.user import UserChangePassword


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    async def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter_by(id=user_id).first()

    async def get_user_by_email(self, email) -> User:
        return self.db.query(User).filter_by(email=email).first()

    async def get_user_by_username(self, username) -> User:
        return self.db.query(User).filter_by(username=username).first()

    async def update_user(
        self, user_id: int, user_update: UserUpdateIn | UserChangePassword
    ) -> User:
        query = self.db.query(User).filter(User.id == user_id)
        query.update(user_update.dict(exclude_unset=True), synchronize_session=False)
        user = query.first()
        self.db.commit()
        self.db.refresh(user)

        return user

    async def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
