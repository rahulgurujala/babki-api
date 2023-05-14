from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import oauth2, schemas, utils
from app.database import get_db
from app.models import User
from app.repositories import UserRepository


async def create_user(
    user_create: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """Creates user"""

    user_repository = UserRepository(db)

    if await user_repository.get_user_by_email():
        raise HTTPException(status_code=400, detail="A user with that email exists.")

    user = User(**user_create.dict())
    user.password = utils.hash(user_create.password)

    return await user_repository.create_user(user)


async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Gets a user by id"""

    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail=f"User does not exist.")

    if user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    return user


async def update_user(
    user_id: int,
    user_update: schemas.UserUpdateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.UserUpdateOut:
    """Updates user info"""

    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail=f"User does not exist.")

    if user != current_user:
        print("compare works")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    if user_repository.get_user_by_email(user_update.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email was found.",
        )

    user_repository.update_user(user_id, user_update)

    return user


async def change_password(
    user_id: int,
    user_update: schemas.UserChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Changes user's password"""

    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_id(user_id)

    if user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    user_update.password = utils.hash(user_update.password)
    user_repository.update_user(user_id, user_update)

    return Response(status_code=200)


async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    """Deletes user"""

    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail=f"User does not exist.")

    if user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    return await user_repository.delete_user(user)
