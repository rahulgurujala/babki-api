from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud.account import account_crud
from app.models import Account


def create(user_id: int, account_create: schemas.AccountCreate, db: Session):
    account = Account(**account_create.dict(), user_id=user_id)

    return account_crud.create(db, account)


def get_account_by_id(user_id: int, account_id: int, db: Session):
    account: Account = account_crud.get_account(db, account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return account


def get_all(user_id: int, db: Session):
    return account_crud.get_all_accounts(db, user_id)


def update(
    user_id: int, account_id: int, account_update: schemas.AccountUpdate, db: Session
):
    account = account_crud.get_account(db, account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return account_crud.update(db, account_id, account_update)


def delete(user_id: int, account_id: int, db: Session):
    account = account_crud.get_account(db, account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return account_crud.delete(db, account)
