from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, utils
from app.models import User


def create(user_create: schemas.UserCreate, db: Session):
    """Creates user"""

    if crud.user.get_user_by_email(db, user_create.email):
        raise HTTPException(status_code=400, detail="A user with that email exists.")

    user = User(**user_create.dict())
    user.password = utils.hash(user_create.password)

    return crud.user.create(user)


def get_user(user_id: int, db: Session):
    """Gets a user"""

    user = crud.user.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    return user


def update(user: User, user_update: schemas.UserUpdateIn, db: Session):
    """Updates user info"""

    if user_update.email and crud.user.get_user_by_email(user_update.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email was found.",
        )

    return crud.user.update(user, user_update)


def change_password(user: User, user_update: schemas.UserChangePassword, db: Session):
    """Changes user's password"""

    user_update.password = utils.hash(user_update.password)

    return crud.user.update(user, user_update)


def delete(user: User, db: Session):
    """Deletes user"""

    return crud.user.delete(user)
