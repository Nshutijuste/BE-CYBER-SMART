import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_auth_service
from app.main import app
from app.services.auth_service import AuthService
from tests.fakes import FakePasswordHasher, FakeUserRepository

URL = "/api/v1/auth/register"
PASSWORD = "a long enough passphrase"


@pytest.fixture
def users():
    return FakeUserRepository()


@pytest.fixture
def client(users):
    service = AuthService(users, FakePasswordHasher())
    app.dependency_overrides[get_auth_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_register_returns_201_and_only_an_id(client, users):
    response = client.post(URL, json={"email": "ann@example.com", "password": PASSWORD})
    assert response.status_code == 201
    assert list(response.json()) == ["id"]
    assert len(users.rows) == 1


def test_response_never_contains_the_password_or_its_hash(client):
    response = client.post(URL, json={"email": "ann@example.com", "password": PASSWORD})
    assert PASSWORD not in response.text
    assert "hashed:" not in response.text


def test_taken_email_gives_409_with_a_safe_message(client):
    client.post(URL, json={"email": "ann@example.com", "password": PASSWORD})
    response = client.post(URL, json={"email": "ann@example.com", "password": PASSWORD})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "account_unavailable"


def test_short_password_gives_422_and_is_not_echoed(client):
    response = client.post(URL, json={"email": "ann@example.com", "password": "tooshort"})
    assert response.status_code == 422
    assert "tooshort" not in response.text


def test_unknown_field_gives_422(client):
    response = client.post(
        URL, json={"email": "ann@example.com", "password": PASSWORD, "role": "system_admin"}
    )
    assert response.status_code == 422


def test_missing_email_and_phone_gives_422(client):
    response = client.post(URL, json={"password": PASSWORD})
    assert response.status_code == 422