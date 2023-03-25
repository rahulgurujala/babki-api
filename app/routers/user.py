from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import oauth2
from app.database import get_db

from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["Users"])


# @router.get("/", status_code=status.HTTP_200_OK)
# def get_users(db: Session = Depends(get_db)) -> list[schemas.User]:
#     """Returns all users"""

#     users = db.query(models.User).all()

#     return users


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)) -> schemas.User:
    """Returns single user"""

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
        )

    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """Creates user"""

    user_query = db.query(models.User).filter(models.User.email == user.email)

    if user_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is taken."
        )

    # Hash user's password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    user_update: schemas.UserUpdateIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.UserUpdateOut:
    """Updates user"""

    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User does not exist.",
        )

    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    if user_update.email and user.email == user_update.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email was found.",
        )

    user_query.update(user_update.dict(exclude_unset=True), synchronize_session=False)
    db.commit()

    return user
