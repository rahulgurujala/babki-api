import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, schemas
from app.config import settings
from app.database import get_db
from app.main import app
from app.models import Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
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


@pytest.fixture
def test_user2(client, session):
    user_data = {"username": "test2", "email": "test2@gmail.com", "password": "test123"}
    res = client.post(
        "/user",
        json=user_data,
    )
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    token, _ = create_access_token({"user_id": test_user["id"]})

    return token


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_accounts(test_user, test_user2, session):
    """Creates accounts on the database"""

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

    accounts = [models.Account(**account) for account in accounts_data]

    session.add_all(accounts)
    session.commit()

    accounts = session.query(models.Account).all()
    return accounts


@pytest.fixture
def test_transaction(test_user, test_accounts, session):
    """Creates test transactions on the database"""

    transaction = {"user_id": 1, "account_id": 1, "amount": 2000, "is_debit": False}
    transaction = models.Transaction(**transaction)

    session.add(transaction)
    session.commit()

    transaction = session.query(models.Transaction).all()

    return transaction


@pytest.fixture
def update_account_data():
    return {"account_name": "New account", "balance": 400}
