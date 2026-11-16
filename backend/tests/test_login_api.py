import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_login_service
from app.main import app
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService
from app.services.login_service import LoginService
from tests.fakes import (
    FakeLoginAttemptRepository,
    FakePasswordHasher,
    FakeUserRepository,
)

URL = "/api/v1/auth/login"
PASSWORD = "a long enough passphrase"


@pytest.fixture
def attempts():
    return FakeLoginAttemptRepository()


@pytest.fixture
def client(attempts):
    users = FakeUserRepository()
    hasher = FakePasswordHasher()
    AuthService(users, hasher).register(
        RegisterRequest(email="ann@example.com", password=PASSWORD)
    )
    service = LoginService(users, attempts, hasher)
    app.dependency_overrides[get_login_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_good_login_returns_200_and_only_an_id(client):
    response = client.post(URL, json={"email": "ann@example.com", "password": PASSWORD})
    assert response.status_code == 200
    assert list(response.json()) == ["id"]


def test_wrong_password_and_unknown_account_give_the_same_401(client):
    wrong = client.post(URL, json={"email": "ann@example.com", "password": "wrong password"})
    unknown = client.post(URL, json={"email": "nobody@example.com", "password": PASSWORD})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()
    assert wrong.json()["error"]["code"] == "invalid_credentials"


def test_the_response_never_contains_the_password(client):
    response = client.post(URL, json={"email": "ann@example.com", "password": "wrong password"})
    assert "wrong password" not in response.text


def test_the_source_and_device_are_recorded(client, attempts):
    client.post(
        URL,
        json={"email": "ann@example.com", "password": PASSWORD},
        headers={"user-agent": "UnitTestBrowser/9"},
    )
    assert attempts.rows[0]["device_summary"] == "UnitTestBrowser/9"
    assert attempts.rows[0]["source_ip"]


def test_a_very_long_device_text_is_cut_short(client, attempts):
    client.post(
        URL,
        json={"email": "ann@example.com", "password": PASSWORD},
        headers={"user-agent": "x" * 500},
    )
    assert len(attempts.rows[0]["device_summary"]) == 200


def test_bad_shape_gives_422(client):
    assert client.post(URL, json={"password": PASSWORD}).status_code == 422
