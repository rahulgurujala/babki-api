from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app import crud, models, oauth2, schemas
from app.database import get_db
from app.services import user as user_service

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """Creates user"""

    user = user_service.create(db, user_create)

    return user


@router.get("/", status_code=status.HTTP_200_OK)
def get_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Returns single user"""

    user = user_service.get_user(db, current_user.id)

    return user


@router.patch("/", status_code=status.HTTP_200_OK)
def update_user(
    user_update: schemas.UserUpdateIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Updates user"""

    user = user_service.update(db, current_user, user_update)

    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Deletes user"""

    user_service.delete(db, current_user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
