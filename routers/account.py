from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db
from app.services import account as account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_account(
    account_create: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Creates user account"""

    try:
        account = await account_service.create(current_user.id, account_create, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

    return account


@router.get("", status_code=200)
@router.get("/", status_code=200, include_in_schema=False)
async def get_all_accounts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Account]:
    """Returns all user accounts"""

    return await account_service.get_all_accounts(current_user.id, db)


@router.get("/{id}", status_code=200)
async def get_account_by_id(
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

    account = await account_service.get_account_by_id(id, db)

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    try:
        account = await account_service.update(id, account_update, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

    return account


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Deletes user account"""

    account = await account_service.get_account_by_id(id, db)

    if account.user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    try:
        account = await account_service.delete(id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
