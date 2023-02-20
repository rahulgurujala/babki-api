from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import models
from ..schemas import *

router = APIRouter(tags=["Users"])


@router.get("/users", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    """Returns all users"""

    users = db.query(models.User).all()

    return users


@router.get("/user/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    """Returns single user"""

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist."
        )

    return user


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(User: UserIn, db: Session = Depends(get_db)):
    """Creates user"""

    user = db.query(models.User).filter(models.User.email == User.email).first()

    if user:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists."
        )

    new_user = models.User(**User.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"data": new_user}
