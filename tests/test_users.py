import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users",
        json={"username": "test", "email": "test@gmail.com", "password": "test123"},
    )
    assert res.json().get("username") == "test"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "test123", 403),
        ("test@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "test123", 422),
        ("test@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200

    res = schemas.Token(**res.json())
    payload = jwt.decode(res.access_token, settings.SECRET_KEY, settings.ALGORITHM)
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert res.token_type == "Bearer"


def test_login_user_wrong_credentials(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": "wrongpassword123"}
    )

    assert res.status_code == 403
