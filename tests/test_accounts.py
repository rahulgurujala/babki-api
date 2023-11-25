import pytest

from app import schemas


def test_get_all_accounts(authorized_client, test_accounts):
    res = authorized_client.get("/accounts")

    assert res.status_code == 200


def test_unauthorized_client_get_all_accounts(client, test_accounts):
    res = client.get("/accounts")

    assert res.status_code == 401


def test_unauthorized_client_get_one_account(client, test_accounts):
    res = client.get(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 401


def test_get_account_not_exist(authorized_client, test_accounts):
    res = authorized_client.get("/accounts/999")

    assert res.status_code == 404


def test_get_account(authorized_client, test_accounts):
    res = authorized_client.get(f"/accounts/{test_accounts[0].id}")

    account = schemas.Account(**res.json())
    assert res.status_code == 200
    assert account.account_name == test_accounts[0].account_name


@pytest.mark.parametrize(
    "account_name, account_type, balance",
    [("Bank 1", "Cash", 120), ("Bank 2", "Deposit", 150)],
)
def test_create_account(authorized_client, account_name, account_type, balance):
    res = authorized_client.post(
        "/accounts",
        json={
            "account_name": account_name,
            "account_type": account_type,
            "balance": balance,
        },
    )

    schemas.Account(**res.json())
    assert res.status_code == 201


def test_unauthorized_client_create_account(client, test_user):
    res = client.post(
        "/accounts",
        json={
            "account_name": "abcdef",
            "account_type": "abcdef",
            "balance": 12345,
        },
    )

    assert res.status_code == 401


def test_unauthorized_client_delete_account(client, test_user, test_accounts):
    res = client.delete(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 401


def test_delete_account_success(authorized_client, test_accounts):
    res = authorized_client.delete(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 204


def test_delete_account_not_exist(authorized_client, test_accounts):
    res = authorized_client.delete("/accounts/9999")

    assert res.status_code == 404


def test_unauthorized_client_update_account(client, test_user, test_accounts):
    res = client.patch(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 401


def test_update_account_success(authorized_client, test_accounts, update_account_data):
    res = authorized_client.patch(
        f"/accounts/{test_accounts[0].id}", json=update_account_data
    )

    updated_account = schemas.Account(**res.json())
    assert res.status_code == 200
    assert updated_account.account_name == update_account_data["account_name"]
    assert updated_account.balance == update_account_data["balance"]


def test_update_account_not_exist(
    authorized_client, test_accounts, update_account_data
):
    res = authorized_client.patch("/accounts/9999", json=update_account_data)

    assert res.status_code == 404
