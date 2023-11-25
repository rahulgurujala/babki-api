from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import account_crud, transaction_crud
from app.models import Transaction
from app.schemas.account import Account


def create(db: Session, user_id: int, transaction_create: schemas.TransactionCreate):
    account = account_crud.get_account(
        db, transaction_create.account_id, user_id=user_id
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with id: {transaction_create['account_id']} does not exist.",
        )

    # Update account balance
    balance = account_crud.get_balance(db, account.id, user_id)

    if transaction_create.is_debit:
        balance = account_crud.set_balance(
            db, account.id, balance - transaction_create.amount
        )
    else:
        balance = account_crud.set_balance(
            db, account.id, balance + transaction_create.amount
        )

    # Add transaction data
    transaction = transaction_crud.create(
        db, Transaction(**transaction_create.dict(), user_id=user_id)
    )

    return transaction


def get_transaction(db: Session, user_id: int, transaction_id: int):
    transaction = transaction_crud.get_transaction_by_id(db, transaction_id, user_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction does not exist.")

    return transaction


def get_account_transactions(db: Session, user_id: int, account_id: int):
    account = account_crud.get_account(db, account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    transactions = transaction_crud.get_account_transactions(
        db, account_id, sorted=True
    )

    return transactions


def get_all_transactions(db: Session, user_id: int):
    transactions = transaction_crud.get_all_transactions(db, user_id, sorted=True)

    return transactions


def update(
    db: Session,
    user_id: int,
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
):
    old_transaction = transaction_crud.get_transaction_by_id(
        db, transaction_id, user_id
    )

    if not old_transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    account: Account = old_transaction.account
    balance = account_crud.get_balance(db, account.id, account.user_id)

    # Undo previous transaction
    if old_transaction.is_debit:
        balance = account_crud.set_balance(
            db, account.id, balance + old_transaction.amount
        )
    else:
        balance = account_crud.set_balance(
            db, account.id, balance - old_transaction.amount
        )

    # Process new transaction
    if transaction_update.is_debit:
        balance = account_crud.set_balance(
            db, account.id, balance - transaction_update.amount
        )
    else:
        balance = account_crud.set_balance(
            db, account.id, balance + transaction_update.amount
        )

    return transaction_crud.update(db, transaction_id, transaction_update)


def delete(db: Session, user_id: int, transaction_id: int):
    transaction = transaction_crud.get_transaction_by_id(db, transaction_id, user_id)

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    # Update account balance
    account = account_crud.get_account(db, transaction.account_id, transaction.user_id)
    balance = account_crud.get_balance(db, account.id, account.user_id)

    # Undo transaction on account
    if transaction.is_debit:
        account_crud.set_balance(db, account.id, balance + transaction.amount)
    else:
        account_crud.set_balance(db, account.id, balance - transaction.amount)

    return transaction_crud.delete(db, transaction)
