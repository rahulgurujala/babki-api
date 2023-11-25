from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, utils
from app.crud import user_crud
from app.models import User


def create(db: Session, user_create: schemas.UserCreate):
    """Creates user"""

    if user_crud.get_user_by_email(db, user_create.email):
        raise HTTPException(status_code=400, detail="A user with that email exists.")

    user = User(**user_create.dict())
    user.password = utils.hash(user_create.password)

    return user_crud.create(db, user)


def get_user(db: Session, user_id: int):
    """Gets a user"""

    user = user_crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    return user


def update(db: Session, user: User, user_update: schemas.UserUpdateIn):
    """Updates user info"""

    if user_update.email and user_crud.get_user_by_email(db, user_update.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email was found.",
        )

    return user_crud.update(db, user, user_update)


def change_password(db: Session, user: User, user_update: schemas.UserChangePassword):
    """Changes user's password"""

    user_update.password = utils.hash(user_update.password)

    return user_crud.update(db, user, user_update)


def delete(db: Session, user: User):
    """Deletes user"""

    return user_crud.delete(db, user)
