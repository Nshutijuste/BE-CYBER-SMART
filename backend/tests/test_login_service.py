import pytest
from pydantic import ValidationError

from app.core.crypto import KeyedHasher
from app.core.errors import AuthenticationError, TooManyAttemptsError
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService
from app.services.login_service import LoginService
from tests.fakes import (
    FakeBreachChecker,
    FakeClock,
    FakeLoginAttemptRepository,
    FakeMfaRepository,
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
    mfa = FakeMfaRepository()
    hasher = FakePasswordHasher()
    clock = FakeClock()
    AuthService(users, hasher, FakeBreachChecker()).register(
        RegisterRequest(email="ann@example.com", phone="+250781000000", password=PASSWORD)
    )
    service = LoginService(users, attempts, mfa, hasher, KeyedHasher("test-secret-x"), clock)
    return service, users, attempts, mfa, hasher, clock


def login(service, **fields):
    data = {"password": PASSWORD, **fields}
    return service.login(LoginRequest(**data), source_ip=IP, device_summary=DEVICE)


def wrong(service, email="ann@example.com"):
    with pytest.raises(AuthenticationError):
        login(service, email=email, password="not the right one")


def test_right_email_and_password_succeeds_and_is_recorded(world):
    service, users, attempts, *_ = world
    outcome = login(service, email="ann@example.com")
    assert outcome.user_id == users.rows[0]["id"]
    assert outcome.needs_mfa is False
    row = attempts.rows[0]
    assert (row["success"], row["failure_reason"], row["source_ip"]) == (True, None, IP)
    assert row["device_summary"] == DEVICE
    assert row["identifier_hash"] and "ann@example.com" not in row["identifier_hash"]


def test_email_is_not_case_sensitive(world):
    service, *_ = world
    assert login(service, email="ANN@Example.com")


def test_login_by_phone_works(world):
    service, *_ = world
    assert login(service, phone="+250781000000")


def test_wrong_password_is_refused_and_recorded(world):
    service, users, attempts, *_ = world
    wrong(service)
    assert attempts.rows[0]["failure_reason"] == "wrong_password"
    assert attempts.rows[0]["user_id"] == users.rows[0]["id"]


def test_unknown_account_is_refused_recorded_and_wastes_the_same_time(world):
    service, _, attempts, _, hasher, _ = world
    wrong(service, email="nobody@example.com")
    assert attempts.rows[0]["failure_reason"] == "unknown_account"
    assert attempts.rows[0]["user_id"] is None
    assert hasher.dummy_calls == 1


def test_the_error_is_identical_for_unknown_account_and_wrong_password(world):
    service, *_ = world
    with pytest.raises(AuthenticationError) as unknown:
        login(service, email="nobody@example.com")
    with pytest.raises(AuthenticationError) as bad:
        login(service, email="ann@example.com", password="not the right one")
    assert (unknown.value.message, unknown.value.code) == (bad.value.message, bad.value.code)
    assert unknown.value.status_code == bad.value.status_code == 401


def test_a_deactivated_account_is_refused_even_with_the_right_password(world):
    service, users, attempts, *_ = world
    users.deactivate(users.rows[0]["id"])
    with pytest.raises(AuthenticationError):
        login(service, email="ann@example.com")
    assert attempts.rows[0]["failure_reason"] == "inactive_account"


def test_the_password_is_never_written_to_the_attempt_log(world):
    service, _, attempts, *_ = world
    wrong(service)
    assert "not the right one" not in str(attempts.rows)


def test_five_failures_then_a_wait_even_for_the_right_password(world):
    service, _, attempts, *_ = world
    for _ in range(5):
        wrong(service)
    with pytest.raises(TooManyAttemptsError) as blocked:
        login(service, email="ann@example.com")  # the RIGHT password
    assert blocked.value.retry_after == 30
    assert blocked.value.headers == {"Retry-After": "30"}
    assert attempts.rows[-1]["failure_reason"] == "throttled"


def test_the_wait_ends_and_a_success_clears_the_count(world):
    service, _, _, _, _, clock = world
    for _ in range(5):
        wrong(service)
    clock.advance(seconds=31)
    assert login(service, email="ann@example.com")
    for _ in range(4):  # a fresh count: four more failures are still free
        wrong(service)
    assert login(service, email="ann@example.com")


def test_the_wait_grows_with_more_failures(world):
    service, _, _, _, _, clock = world
    for _ in range(5):
        wrong(service)
    clock.advance(seconds=31)
    wrong(service)  # the 6th failure
    with pytest.raises(TooManyAttemptsError) as blocked:
        login(service, email="ann@example.com")
    assert blocked.value.retry_after == 60


def test_an_invented_account_is_locked_exactly_like_a_real_one(world):
    service, *_ = world
    for _ in range(5):
        wrong(service, email="nobody@example.com")
    with pytest.raises(TooManyAttemptsError) as blocked:
        login(service, email="nobody@example.com")
    assert blocked.value.retry_after == 30  # same as the real account in the test above


def test_hammering_while_locked_does_not_make_the_wait_longer(world):
    service, *_ = world
    for _ in range(5):
        wrong(service)
    for _ in range(30):
        with pytest.raises(TooManyAttemptsError) as blocked:
            login(service, email="ann@example.com")
    assert blocked.value.retry_after == 30


def test_login_says_when_a_second_step_is_needed(world):
    service, users, _, mfa, *_ = world
    mfa.rows[users.rows[0]["id"]] = {"secret_encrypted": "x", "enabled": True, "last_step": 0}
    assert login(service, email="ann@example.com").needs_mfa is True


def test_login_needs_exactly_one_identifier():
    with pytest.raises(ValidationError):
        LoginRequest(password=PASSWORD)
    with pytest.raises(ValidationError):
        LoginRequest(email="ann@example.com", phone="+250781000000", password=PASSWORD)
