from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import oauth2, schemas, utils
from app.database import get_db
from app.models import User
from app.repositories import UserRepository


async def create(
    user_create: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """Creates user"""

    user_repository = UserRepository(db)

    if await user_repository.get_user_by_email():
        raise HTTPException(status_code=400, detail="A user with that email exists.")

    user = User(**user_create.dict())
    user.password = utils.hash(user_create.password)

    return await user_repository.create(user)


async def get_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Gets a user"""

    user_repository = UserRepository(db)

    return await user_repository.get_user_by_id(current_user.id)


async def update(
    user_update: schemas.UserUpdateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.UserUpdateOut:
    """Updates user info"""

    user_repository = UserRepository(db)

    if user_update.email and user_repository.get_user_by_email(user_update.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email was found.",
        )

    return await user_repository.update(current_user, user_update)


async def change_password(
    user_update: schemas.UserChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Changes user's password"""

    user_repository = UserRepository(db)
    user_update.password = utils.hash(user_update.password)

    return await user_repository.update(current_user, user_update)


async def delete(
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    """Deletes user"""

    user_repository = UserRepository(db)

    return await user_repository.delete(current_user)
