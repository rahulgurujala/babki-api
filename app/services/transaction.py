from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.models import Transaction
from app.repositories import AccountRepository, TransactionRepository


async def create(transaction_create: schemas.TransactionCreate, db: Session):
    account_repository = AccountRepository(db)
    account = await account_repository.get_account(
        transaction_create.account_id, transaction_create.user_id
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with id: {transaction_create.account_id} does not exist.",
        )

    # Update account balance
    balance = await account_repository.get_balance(account.id, account.user_id)
    balance = await account_repository.set_balance(
        account.id, balance - transaction_create.amount
    )

    # Add transaction data
    transaction_repository = TransactionRepository(db)
    transaction = Transaction(**transaction_create.dict())
    transaction = await transaction_repository.create(transaction)

    return transaction


async def get_transaction(user_id: int, transaction_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    transaction = await transaction_repository.get_transaction_by_id(
        transaction_id, user_id
    )

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction does not exist.")

    return transaction


async def get_account_transactions(user_id: int, account_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    account_repository = AccountRepository(db)
    account = await account_repository.get_account(account_id, user_id)

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
    transaction = await transaction_repository.get_transaction_by_id(
        transaction_id, transaction_update.user_id
    )

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    # Update account balance
    account_repository = AccountRepository(db)
    account = await account_repository.get_account(
        transaction.account_id, transaction.user_id
    )

    balance = await account_repository.get_balance(account.id, account.user_id)
    balance = await account_repository.set_balance(
        account.id, balance - transaction_update.amount
    )

    if transaction.is_debit:
        await account_repository.set_balance(
            account.id, balance - transaction_update.amount
        )
    else:
        await account_repository.set_balance(
            account.id, balance + transaction_update.amount
        )

    return await transaction_repository.update(transaction_id, transaction_update)


async def delete(user_id: int, transaction_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    transaction: Transaction = await transaction_repository.get_transaction_by_id(
        transaction_id, user_id
    )

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    # Update account balance
    account_repository = AccountRepository(db)
    account = await account_repository.get_account(
        transaction.account_id, transaction.user_id
    )
    balance = await account_repository.get_balance(account.id, account.user_id)

    if transaction.is_debit:
        await account_repository.set_balance(account.id, balance - transaction.amount)
    else:
        await account_repository.set_balance(account.id, balance - transaction.amount)

    return await transaction_repository.delete(transaction)
