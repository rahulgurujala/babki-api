import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import get_db
from app.main import app
from app.models import Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"username": "test", "email": "test@gmail.com", "password": "test123"}
    res = client.post(
        "/user",
        json=user_data,
    )
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture()
def test_user2(client):
    user_data = {"username": "test2", "email": "test2@gmail.com", "password": "test123"}
    res = client.post(
        "/user",
        json=user_data,
    )
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture()
def test_accounts(test_user, test_user2, session):
    accounts_data = [
        {
            "account_type": "Cash",
            "account_name": "Bank 1",
            "balance": 500,
            "user_id": test_user["id"],
        },
        {
            "account_type": "Deposit",
            "account_name": "Bank 2",
            "balance": 500,
            "user_id": test_user["id"],
        },
        {
            "account_type": "Checking",
            "account_name": "Bank 3",
            "balance": 500,
            "user_id": test_user["id"],
        },
        {
            "account_type": "Checking",
            "account_name": "Bank 3",
            "balance": 500,
            "user_id": test_user2["id"],
        },
    ]

    def create_account_model(account):
        return models.Account(**account)

    accounts_map = map(create_account_model, accounts_data)
    accounts = list(accounts_map)

    session.add_all(accounts)
    session.commit()

    accounts = session.query(models.Account).all()
    return accounts


@pytest.fixture()
def test_transactions(test_user, test_accounts, session):
    transactions_data = [
        {"user_id": 1, "account_id": 1, "amount": 2000, "is_debit": False},
    ]

    def create_transaction_model(transaction):
        return models.Transaction(**transaction)

    transactions_map = map(create_transaction_model, transactions_data)
    transactions = list(transactions_map)

    session.add_all(transactions)
    session.commit()

    transactions = session.query(models.Transaction).all()
    return transactions


@pytest.fixture()
def update_account_data():
    return {"account_name": "New account", "balance": 400}
