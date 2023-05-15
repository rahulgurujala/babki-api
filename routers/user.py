from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_user(
    user_create: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """Creates user"""

    try:
        user = await user_service.create(user_create, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

    return user


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Returns single user"""

    user = await user_service.get_user(id, db)

    return user


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    id: int,
    user_update: schemas.UserUpdateIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.User:
    """Updates user"""

    try:
        user = await user_service.update(current_user, user_update, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Deletes user"""

    try:
        await user_service.delete(current_user, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

    raise Response(status_code=status.HTTP_204_NO_CONTENT)
