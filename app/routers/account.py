from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db
from app.services import account as account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_account(
    account_create: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Creates user account"""

    account = account_service.create(db, current_user.id, account_create)

    return account


@router.get("/", status_code=200)
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Account]:
    """Returns all user accounts"""

    return account_service.get_all(db, current_user.id)


@router.get("/{id}", status_code=200)
def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Return single user account"""

    return account_service.get_account_by_id(db, current_user.id, id)


@router.patch("/{id}", status_code=200)
def update_account(
    id: int,
    account_update: schemas.AccountUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Updates account"""

    account = account_service.get_account_by_id(db, current_user.id, id)

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account = account_service.update(db, current_user.id, id, account_update)

    return account


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Deletes user account"""

    account = account_service.get_account_by_id(db, current_user.id, id)

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account = account_service.delete(db, current_user.id, id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
