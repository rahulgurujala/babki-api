from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("", status_code=status.HTTP_200_OK)
@router.get("/", status_code=status.HTTP_200_OK, include_in_schema=False)
def get_accounts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> list[schemas.Account]:
    """Returns all user accounts"""

    accounts = (
        db.query(models.Account).filter(models.Account.user_id == current_user.id).all()
    )

    return accounts


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Return single user account"""

    account = (
        db.query(models.Account)
        .filter(models.Account.id == id, models.Account.user_id == current_user.id)
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account does not exist."
        )

    return account


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_account(
    account_create: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Creates user account"""

    account = models.Account(**account_create.dict(), user_id=current_user.id)
    db.add(account)
    db.commit()
    db.refresh(account)

    return account


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_account(
    id: int,
    account_update: schemas.AccountUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Updates account"""

    account_query = db.query(models.Account).filter(models.Account.id == id)
    account = account_query.first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account does not exist.",
        )

    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account_query.update(
        account_update.dict(exclude_unset=True), synchronize_session=False
    )
    db.commit()

    return account


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Deletes user account"""

    account_query = db.query(models.Account).filter(models.Account.id == id)
    account = account_query.first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account does not exist.",
        )

    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
