from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db

from .. import models, oauth2, schemas

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", status_code=status.HTTP_200_OK)
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


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_account(
    Account: schemas.AccountCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Creates user account"""

    account = models.Account(**Account.dict(), user=current_user)
    db.add(account)
    db.commit()
    db.refresh(account)

    return account


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_account(
    id: int,
    account: schemas.AccountUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schemas.Account:
    """Updates account"""

    account_query = db.query(models.Account).filter(
        models.Account.id == id, models.Account.user_id == current_user.id
    )

    if not account_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account does not exist.",
        )

    if account_query.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account_query.update(account.dict(exclude_unset=True), synchronize_session=False)
    db.commit()

    return account_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Deletes user account"""

    account_query = db.query(models.Account).filter(
        models.Account.id == id, models.Account.user_id == current_user.id
    )

    if not account_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account does not exist.",
        )

    if account_query.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    account_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
