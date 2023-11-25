import pytest

from app import models, schemas
from tests.conftest import test_user2


def test_get_all_transactions(authorized_client, test_transaction):
    res = authorized_client.get("/transactions")

    assert res.status_code == 200
    assert len(res.json()) == len(test_transaction)


def test_get_account_transactions(authorized_client, test_accounts, test_transaction):
    res = authorized_client.get(
        "/transactions", params={"account_id": test_accounts[0].id}
    )

    assert res.status_code == 200


def test_get_transaction(authorized_client, test_transaction):
    res = authorized_client.get("/transactions/1")

    assert res.status_code == 200


def test_create_transaction(authorized_client, test_accounts):
    old_balance = test_accounts[0].balance
    res = authorized_client.post(
        "/transactions",
        json={"user_id": 1, "account_id": 1, "amount": 250, "is_debit": True},
    )

    transaction = schemas.Transaction(**res.json())
    assert res.status_code == 201
    assert transaction.amount == 250
    assert transaction.is_debit == True

    new_balance = transaction.account.balance
    assert transaction.amount == old_balance - new_balance

    res = authorized_client.get(f"/accounts/{test_accounts[0].id}")
    assert res.json()["balance"] == new_balance


def test_create_transaction_unauthorized_user(client):
    transaction_data = {"user_id": 1, "account_id": 1, "amount": 250, "is_debit": True}
    res = client.post(
        "/transactions",
        json=transaction_data,
    )

    assert res.status_code == 401


def test_update_transaction(authorized_client, test_accounts):
    # Create new transaction
    transaction = {
        "category": "Groceries",
        "account_id": 1,
        "amount": 1000,
        "is_debit": False,
    }

    initial_balance = authorized_client.get(f"/accounts/1").json()["balance"]

    res = authorized_client.post(
        f"/transactions",
        json=transaction,
    )

    assert res.status_code == 201
    transaction = res.json()

    # Update created transaction
    transaction["amount"] = 1500

    res = authorized_client.patch(
        f"/transactions/{transaction['id']}",
        json=transaction,
    )

    assert res.status_code == 200
    updated_transaction = schemas.Transaction(**res.json())
    assert updated_transaction.amount == transaction["amount"]
    assert updated_transaction.category == "Groceries"

    assert (
        updated_transaction.account.balance == initial_balance + transaction["amount"]
    )


# test update transaction not exist
def test_update_transaction_not_exist(authorized_client):
    transaction = {
        "category": "Groceries",
        "account_id": 1,
        "amount": 1000,
        "is_debit": False,
    }
    res = authorized_client.patch("/transactions/1", json=transaction)

    assert res.status_code == 404


# test delete transaction
def test_delete_transaction(authorized_client, test_transaction, session):
    res = authorized_client.delete(f"/transactions/{test_transaction[0].id}")

    assert res.status_code == 204
    assert len(session.query(models.Transaction).all()) == 0


# test delete transaction not exist
def test_delete_transaction_not_exist(authorized_client):
    res = authorized_client.delete("/transactions/1")

    assert res.status_code == 404
