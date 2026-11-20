import uuid

import pyotp
import pytest

from app.core.crypto import FieldCipher, KeyedHasher
from app.core.errors import (
    AuthenticationError,
    MfaAlreadyEnabledError,
    TooManyAttemptsError,
)
from app.services.mfa_service import MfaService
from tests.fakes import FakeClock, FakeLoginAttemptRepository, FakeMfaRepository

SECRET = "a-test-secret-long-enough"
IP = "203.0.113.7"


@pytest.fixture
def world():
    mfa, attempts, clock = FakeMfaRepository(), FakeLoginAttemptRepository(), FakeClock()
    service = MfaService(mfa, attempts, FieldCipher(SECRET), KeyedHasher(SECRET), clock)
    return service, mfa, attempts, clock, uuid.uuid4()


def good_code(secret, clock, shift=0.0):
    return pyotp.TOTP(secret).at(clock.now.timestamp() + shift)


def bad_code(secret, clock):
    valid = {good_code(secret, clock, s) for s in (-30, 0, 30)}
    return next(c for c in ("000000", "111111", "222222") if c not in valid)


def enable(service, clock, user_id):
    setup = service.begin_setup(user_id, "ann@example.com")
    service.confirm_setup(user_id, good_code(setup.secret, clock), source_ip=IP)
    return setup.secret


def test_setup_stores_the_secret_encrypted_and_gives_a_link(world):
    service, mfa, _, _, user_id = world
    setup = service.begin_setup(user_id, "ann@example.com")
    assert setup.otpauth_uri.startswith("otpauth://totp/")
    stored = mfa.rows[user_id]["secret_encrypted"]
    assert setup.secret not in stored and stored.startswith("v1.")
    assert mfa.rows[user_id]["enabled"] is False


def test_the_right_code_turns_the_second_step_on(world):
    service, mfa, _, clock, user_id = world
    enable(service, clock, user_id)
    assert mfa.rows[user_id]["enabled"] is True
    assert mfa.rows[user_id]["last_step"] > 0


def test_a_wrong_code_does_not_turn_it_on(world):
    service, mfa, _, clock, user_id = world
    setup = service.begin_setup(user_id, "ann@example.com")
    with pytest.raises(AuthenticationError):
        service.confirm_setup(user_id, bad_code(setup.secret, clock), source_ip=IP)
    assert mfa.rows[user_id]["enabled"] is False


def test_setup_is_refused_when_it_is_already_on(world):
    service, _, _, clock, user_id = world
    enable(service, clock, user_id)
    with pytest.raises(MfaAlreadyEnabledError):
        service.begin_setup(user_id, "ann@example.com")


def test_a_login_code_works_once_and_the_next_period_works_again(world):
    service, _, _, clock, user_id = world
    secret = enable(service, clock, user_id)
    clock.advance(seconds=30)
    code = good_code(secret, clock)
    service.verify_login_code(user_id, code, source_ip=IP)
    with pytest.raises(AuthenticationError):
        service.verify_login_code(user_id, code, source_ip=IP)  # replay
    clock.advance(seconds=30)
    service.verify_login_code(user_id, good_code(secret, clock), source_ip=IP)


def test_a_step_rejected_by_the_atomic_claim_is_not_accepted(world):
    service, mfa, attempts, clock, user_id = world
    secret = enable(service, clock, user_id)
    clock.advance(seconds=30)
    mfa.reject_next_step = True

    with pytest.raises(AuthenticationError):
        service.verify_login_code(user_id, good_code(secret, clock), source_ip=IP)

    assert attempts.rows[-1]["failure_reason"] == "mfa_failed"


def test_a_setup_confirmation_losing_the_atomic_claim_is_rejected(world):
    service, mfa, attempts, clock, user_id = world
    setup = service.begin_setup(user_id, "ann@example.com")
    mfa.reject_next_activation = True

    with pytest.raises(AuthenticationError):
        service.confirm_setup(user_id, good_code(setup.secret, clock), source_ip=IP)

    assert attempts.rows[-1]["failure_reason"] == "mfa_failed"
    assert mfa.rows[user_id]["enabled"] is False


def test_wrong_codes_are_recorded_and_lock_out_guessing(world):
    service, _, attempts, clock, user_id = world
    secret = enable(service, clock, user_id)
    clock.advance(seconds=30)
    for _ in range(5):
        with pytest.raises(AuthenticationError):
            service.verify_login_code(user_id, bad_code(secret, clock), source_ip=IP)
    assert [r["failure_reason"] for r in attempts.rows].count("mfa_failed") == 5
    with pytest.raises(TooManyAttemptsError):  # even the RIGHT code now has to wait
        service.verify_login_code(user_id, good_code(secret, clock), source_ip=IP)


def test_login_code_without_a_second_step_is_refused(world):
    service, _, _, _, user_id = world
    with pytest.raises(AuthenticationError):
        service.verify_login_code(user_id, "123456", source_ip=IP)
