import pytest

from app import schemas


async def test_get_all_accounts(authorized_client, test_accounts):
    res = await authorized_client.get("/accounts")

    async def validate(accounts):
        return [schemas.Account(**account) for account in accounts]

    accounts = validate(res.json())
    assert res.status_code == 200


async def test_unauthorized_client_get_all_accounts(client, test_accounts):
    res = await client.get("/accounts")

    assert res.status_code == 401


async def test_unauthorized_client_get_one_account(client, test_accounts):
    res = await client.get(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 401


async def test_get_account_not_exist(authorized_client, test_accounts):
    res = await authorized_client.get("/accounts/999")

    assert res.status_code == 404


async def test_get_account(authorized_client, test_accounts):
    res = await authorized_client.get(f"/accounts/{test_accounts[0].id}")

    account = schemas.Account(**res.json())
    assert res.status_code == 200
    assert account.account_name == test_accounts[0].account_name


@pytest.mark.parametrize(
    "account_name, account_type, balance",
    [("Bank 1", "Cash", 120), ("Bank 2", "Deposit", 150)],
)
async def test_create_account(authorized_client, account_name, account_type, balance):
    res = await authorized_client.post(
        "/accounts",
        json={
            "account_name": account_name,
            "account_type": account_type,
            "balance": balance,
        },
    )

    created_account = schemas.Account(**res.json())
    assert res.status_code == 201


async def test_unauthorized_client_create_account(client, test_user):
    res = await client.post(
        "/accounts",
        json={
            "account_name": "abcasync def",
            "account_type": "abcasync def",
            "balance": 12345,
        },
    )

    assert res.status_code == 401


async def test_unauthorized_client_delete_account(client, test_user, test_accounts):
    res = await client.delete(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 401


async def test_delete_account_success(authorized_client, test_accounts):
    res = await authorized_client.delete(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 204


async def test_delete_account_not_exist(authorized_client, test_accounts):
    res = await authorized_client.delete("/accounts/9999")

    assert res.status_code == 404


async def test_delete_other_user_account(authorized_client, test_accounts):
    res = await authorized_client.delete(f"/accounts/{test_accounts[3].id}")

    assert res.status_code == 403


async def test_unauthorized_client_update_account(client, test_user, test_accounts):
    res = await client.patch(f"/accounts/{test_accounts[0].id}")

    assert res.status_code == 401


async def test_update_account_success(
    authorized_client, test_accounts, update_account_data
):
    res = await authorized_client.patch(
        f"/accounts/{test_accounts[0].id}", json=update_account_data
    )

    updated_account = schemas.Account(**res.json())
    assert res.status_code == 200
    assert updated_account.account_name == update_account_data["account_name"]
    assert updated_account.balance == update_account_data["balance"]


async def test_update_account_not_exist(
    authorized_client, test_accounts, update_account_data
):
    res = await authorized_client.patch("/accounts/9999", json=update_account_data)

    assert res.status_code == 404


async def test_update_other_user_account(
    authorized_client, test_accounts, update_account_data
):
    res = await authorized_client.patch(
        f"/accounts/{test_accounts[3].id}", json=update_account_data
    )

    assert res.status_code == 403
