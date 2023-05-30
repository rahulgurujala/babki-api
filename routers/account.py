from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db
from app.services import account as account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_account(
    account_create: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Creates user account"""

    account = await account_service.create(current_user.id, account_create, db)

    return account


@router.get("/", status_code=200)
async def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Account]:
    """Returns all user accounts"""

    return await account_service.get_all(current_user.id, db)


@router.get("/{id}", status_code=200)
async def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Return single user account"""

    return await account_service.get_account_by_id(current_user.id, id, db)


@router.patch("/{id}", status_code=200)
async def update_account(
    id: int,
    account_update: schemas.AccountUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Updates account"""

    account = await account_service.get_account_by_id(current_user.id, id, db)

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account = await account_service.update(current_user.id, id, account_update, db)

    return account


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Deletes user account"""

    account = await account_service.get_account_by_id(current_user.id, id, db)

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account = await account_service.delete(current_user.id, id, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
