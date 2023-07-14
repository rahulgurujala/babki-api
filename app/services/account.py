from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.models import Account
from app.repositories import AccountRepository


def create(user_id: int, account_create: schemas.AccountCreate, db: Session):
    account_repository = AccountRepository(db)
    account = Account(**account_create.dict(), user_id=user_id)

    return account_repository.create(account)


def get_account_by_id(user_id: int, account_id: int, db: Session):
    account_repository = AccountRepository(db)
    account = account_repository.get_account(account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return account


def get_all(user_id: int, db: Session):
    account_repository = AccountRepository(db)

    return account_repository.get_all_accounts(user_id)


def update(
    user_id: int, account_id: int, account_update: schemas.AccountUpdate, db: Session
):
    account_repository = AccountRepository(db)
    account = account_repository.get_account(account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return account_repository.update(account_id, account_update)


def delete(user_id: int, account_id: int, db: Session):
    account_repository = AccountRepository(db)
    account = account_repository.get_account(account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return account_repository.delete(account)
