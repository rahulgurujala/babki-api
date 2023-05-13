import pytest

from app import models, schemas
from app.routers.account import get_account


def test_add_transaction(authorized_client, test_accounts):
    res = authorized_client.post(
        "/transactions",
        json={"user_id": 1, "account_id": 1, "amount": 250, "is_debit": True},
    )

    transaction = schemas.Transaction(**res.json())
    assert res.status_code == 201
    assert transaction.amount == 250
    assert transaction.is_debit == True


def test_add_transaction_other_user_account(authorized_client, test_accounts):
    res = authorized_client.post(
        "/transactions",
        json={"user_id": 2, "account_id": 1, "amount": 250, "is_debit": True},
    )

    assert res.status_code == 403


# test add transaction unauthorized
def test_add_transaction_unauthorized_user(client, session, test_accounts):
    transaction_data = {"user_id": 1, "account_id": 1, "amount": 250, "is_debit": True}
    res = client.post(
        "/transactions",
        json=transaction_data,
    )

    accounts = (
        session.query(models.Account)
        .filter(models.Account.id == transaction_data["account_id"])
        .all()
    )
    # TODO: update transaction router to change account account balance
    # account = models.Account(**account)
    # print(test_accounts[0].balance)

    assert res.status_code == 401


# test update transaction.
def test_update_transaction(
    authorized_client, test_accounts, test_transactions, session
):
    transaction = {"amount": 500, "category": "Groceries"}
    account_id, initial_account_balance = test_accounts[0].id, test_accounts[0].balance

    res = authorized_client.patch(
        f"/transactions/{test_accounts[0].user_id}",
        json=transaction,
    )

    updated_transaction = schemas.TransactionUpdate(**res.json())
    assert res.status_code == 200
    assert updated_transaction.amount == transaction["amount"]
    assert updated_transaction.category == "Groceries"

    account = (
        session.query(models.Account)
        .filter(
            models.Account.id == account_id,
            models.User.id == res.json()["user_id"],
        )
        .first()
    )

    assert account.balance == initial_account_balance - transaction["amount"]
    # print(initial_account_balance)


# test update transaction not exist
# test update transaction other user account
# test delete transaction
# test delete transaction not exist
# test delete transaction other user account
