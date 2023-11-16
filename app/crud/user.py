from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserUpdateIn
from app.schemas.user import UserChangePassword


class UserCRUD:
    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_user_by_id(self, db: Session, user_id: int) -> User:
        return db.query(User).filter_by(id=user_id).first()

    def get_user_by_email(self, db: Session, email) -> User:
        return db.query(User).filter_by(email=email).first()

    def get_user_by_username(self, db: Session, username) -> User:
        return db.query(User).filter_by(username=username).first()

    def update(
        self, db: Session, user: User, user_update: UserUpdateIn | UserChangePassword
    ) -> User:
        query = db.query(User).filter_by(id=user.id)
        query.update(user_update.dict(exclude_unset=True), synchronize_session=False)
        user = query.first()
        db.commit()
        db.refresh(user)

        return user

    def delete(self, db: Session, user: User):
        db.delete(user)
        db.commit()


user = UserCRUD()
