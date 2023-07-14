from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.models import Transaction
from app.repositories import AccountRepository, TransactionRepository

# TODO: Fix update transaction logic


def create(user_id: int, transaction_create: schemas.TransactionCreate, db: Session):
    account_repository = AccountRepository(db)
    account = account_repository.get_account(
        transaction_create.account_id, user_id=user_id
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with id: {transaction_create['account_id']} does not exist.",
        )

    # Update account balance
    balance = account_repository.get_balance(account.id, user_id)

    if transaction_create.is_debit:
        balance = account_repository.set_balance(
            account.id, balance - transaction_create.amount
        )
    else:
        balance = account_repository.set_balance(
            account.id, balance + transaction_create.amount
        )

    # Add transaction data
    transaction_repository = TransactionRepository(db)
    transaction = Transaction(**transaction_create.dict(), user_id=user_id)
    transaction = transaction_repository.create(transaction)

    return transaction


def get_transaction(user_id: int, transaction_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    transaction = transaction_repository.get_transaction_by_id(transaction_id, user_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction does not exist.")

    return transaction


def get_account_transactions(user_id: int, account_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    account_repository = AccountRepository(db)
    account = account_repository.get_account(account_id, user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    transactions = transaction_repository.get_account_transactions(account_id)

    transactions = sorted(
        transactions, reverse=True, key=lambda transaction: transaction.created_at
    )

    return transactions


def get_all_transactions(user_id: int, db: Session):
    transaction_repository = TransactionRepository(db)

    transactions = transaction_repository.get_all_transactions(user_id)

    transactions = sorted(
        transactions, reverse=True, key=lambda transaction: transaction.created_at
    )

    return transactions


def update(
    user_id: int,
    transaction_id: int,
    new_transaction: schemas.TransactionUpdate,
    db: Session,
):
    transaction_repository = TransactionRepository(db)
    old_transaction = transaction_repository.get_transaction_by_id(
        transaction_id, user_id
    )

    if not old_transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    account_repository = AccountRepository(db)
    account = account_repository.get_account(
        old_transaction.account_id, old_transaction.user_id
    )
    balance = account_repository.get_balance(account.id, account.user_id)

    # Undo previous transaction
    if old_transaction.is_debit:
        account_repository.set_balance(account.id, balance + old_transaction.amount)
    else:
        account_repository.set_balance(account.id, balance - old_transaction.amount)

    # Process new transaction
    if new_transaction.is_debit:
        account_repository.set_balance(account.id, balance - new_transaction.amount)
    else:
        account_repository.set_balance(account.id, balance + new_transaction.amount)

    transaction = transaction_repository.update(transaction_id, new_transaction)

    return transaction


def delete(user_id: int, transaction_id: int, db: Session):
    transaction_repository = TransactionRepository(db)
    transaction = transaction_repository.get_transaction_by_id(transaction_id, user_id)

    if not transaction:
        raise HTTPException(404, detail=f"Transaction of id: {id} does not exist.")

    # Update account balance
    account_repository = AccountRepository(db)
    account = account_repository.get_account(
        transaction.account_id, transaction.user_id
    )
    balance = account_repository.get_balance(account.id, account.user_id)

    if transaction.is_debit:
        account_repository.set_balance(account.id, balance + transaction.amount)
    else:
        account_repository.set_balance(account.id, balance - transaction.amount)

    return transaction_repository.delete(transaction)
