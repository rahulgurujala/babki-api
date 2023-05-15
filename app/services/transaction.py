from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import oauth2, schemas
from app.database import get_db
from app.models import Transaction
from app.repositories import TransactionRepository


async def create(transaction_create: schemas.TransactionCreate, db: Session):
    transaction_repository = TransactionRepository(db)

    if not await transaction_repository.get_account(transaction_create.account_id):
        raise HTTPException(
            status_code=404,
            detail=f"Account with id: {transaction_create.account_id} does not exist.",
        )

    transaction = Transaction(**transaction_create.dict())

    return await transaction_repository.create(transaction)


async def get_transaction(user_id: int, transaction_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    transaction = await transaction_repository.get_transaction_by_id(
        transaction_id, user_id
    )

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction does not exist.")

    return transaction


async def get_account_transactions(account_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    account = await transaction_repository.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    return await transaction_repository.get_account_transactions(account_id)


async def get_all_transactions(user_id: int, db: Session):
    transaction_repository = TransactionRepository(db)

    return await transaction_repository.get_all_transactions(user_id)


async def update(
    transaction_id: int, transaction_update: schemas.TransactionUpdate, db: Session
):
    transaction_repository = TransactionRepository(db)
    transaction = await transaction_repository.get_transaction_by_id(transaction_id)

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    return await transaction_repository.update(transaction_id, transaction_update)


async def delete(transaction_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    transaction = await transaction_repository.get_transaction_by_id(transaction_id)

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    return await transaction_repository.delete(transaction)
