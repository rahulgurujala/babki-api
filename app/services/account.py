from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.models import Account
from app.repositories import AccountRepository


async def create(account_id: int, account_create: schemas.AccountCreate, db: Session):
    account_repository = AccountRepository(db)
    account = Account(**account_create.dict(), user_id=account_id)

    return await account_repository.create(account)


async def get_account_by_id(user_id: int, account_id: int, db: Session):
    account_repository = AccountRepository(db)
    account = await account_repository.get_account(account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return account


async def get_all(user_id: int, db: Session):
    account_repository = AccountRepository(db)

    return await account_repository.get_all_accounts(user_id)


async def update(
    user_id: int, account_id: int, account_update: schemas.AccountUpdate, db: Session
):
    account_repository = AccountRepository(db)
    account = await account_repository.get_account(account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return await account_repository.update(account_id, account_update)


async def delete(user_id: int, account_id: int, db: Session):
    account_repository = AccountRepository(db)
    account = await account_repository.get_account(account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    if account.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action.",
        )

    return await account_repository.delete(account)
