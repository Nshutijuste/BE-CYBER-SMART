import pytest
from pydantic import ValidationError

from app.core.errors import AuthenticationError
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService
from app.services.login_service import LoginService
from tests.fakes import (
    FakeLoginAttemptRepository,
    FakePasswordHasher,
    FakeUserRepository,
)

PASSWORD = "a long enough passphrase"
IP = "203.0.113.7"
DEVICE = "TestBrowser/1.0"


@pytest.fixture
def world():
    users = FakeUserRepository()
    attempts = FakeLoginAttemptRepository()
    hasher = FakePasswordHasher()
    AuthService(users, hasher).register(
        RegisterRequest(email="ann@example.com", phone="+250781000000", password=PASSWORD)
    )
    return LoginService(users, attempts, hasher), users, attempts, hasher


def login(service, **fields):
    data = {"password": PASSWORD, **fields}
    return service.login(LoginRequest(**data), source_ip=IP, device_summary=DEVICE)


def test_right_email_and_password_succeeds_and_is_recorded(world):
    service, users, attempts, _ = world
    user_id = login(service, email="ann@example.com")
    assert user_id == users.rows[0]["id"]
    assert attempts.rows == [
        {
            "user_id": user_id,
            "source_ip": IP,
            "device_summary": DEVICE,
            "success": True,
            "failure_reason": None,
        }
    ]


def test_email_is_not_case_sensitive(world):
    service, *_ = world
    assert login(service, email="ANN@Example.com")


def test_login_by_phone_works(world):
    service, *_ = world
    assert login(service, phone="+250781000000")


def test_wrong_password_is_refused_and_recorded(world):
    service, users, attempts, _ = world
    with pytest.raises(AuthenticationError):
        login(service, email="ann@example.com", password="not the right one")
    assert attempts.rows[0]["success"] is False
    assert attempts.rows[0]["failure_reason"] == "wrong_password"
    assert attempts.rows[0]["user_id"] == users.rows[0]["id"]


def test_unknown_account_is_refused_recorded_and_wastes_the_same_time(world):
    service, _, attempts, hasher = world
    with pytest.raises(AuthenticationError):
        login(service, email="nobody@example.com")
    assert attempts.rows[0]["failure_reason"] == "unknown_account"
    assert attempts.rows[0]["user_id"] is None
    assert hasher.dummy_calls == 1


def test_the_error_is_identical_for_unknown_account_and_wrong_password(world):
    service, *_ = world
    with pytest.raises(AuthenticationError) as unknown:
        login(service, email="nobody@example.com")
    with pytest.raises(AuthenticationError) as wrong:
        login(service, email="ann@example.com", password="not the right one")
    assert unknown.value.message == wrong.value.message
    assert unknown.value.code == wrong.value.code
    assert unknown.value.status_code == wrong.value.status_code == 401


def test_a_deactivated_account_is_refused_even_with_the_right_password(world):
    service, users, attempts, _ = world
    users.deactivate(users.rows[0]["id"])
    with pytest.raises(AuthenticationError):
        login(service, email="ann@example.com")
    assert attempts.rows[0]["failure_reason"] == "inactive_account"


def test_every_attempt_is_recorded(world):
    service, _, attempts, _ = world
    for _ in range(3):
        with pytest.raises(AuthenticationError):
            login(service, email="ann@example.com", password="nope")
    login(service, email="ann@example.com")
    assert [a["success"] for a in attempts.rows] == [False, False, False, True]


def test_the_password_is_never_written_to_the_attempt_log(world):
    service, _, attempts, _ = world
    with pytest.raises(AuthenticationError):
        login(service, email="ann@example.com", password="secret-guess-12345")
    assert "secret-guess-12345" not in str(attempts.rows)


def test_login_needs_exactly_one_identifier():
    with pytest.raises(ValidationError):
        LoginRequest(password=PASSWORD)
    with pytest.raises(ValidationError):
        LoginRequest(email="ann@example.com", phone="+250781000000", password=PASSWORD)
