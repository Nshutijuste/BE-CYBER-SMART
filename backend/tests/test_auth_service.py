import pytest
from pydantic import ValidationError

from app.core.errors import ConflictError
from app.core.security import Argon2PasswordHasher
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService
from tests.fakes import FakePasswordHasher, FakeUserRepository

GOOD_PASSWORD = "a long enough passphrase"


def make_service() -> tuple[AuthService, FakeUserRepository]:
    users = FakeUserRepository()
    return AuthService(users, FakePasswordHasher()), users


def test_register_stores_a_hash_and_the_subscriber_role():
    service, users = make_service()
    service.register(RegisterRequest(email="Ann@Example.com", password=GOOD_PASSWORD))
    row = users.rows[0]
    assert row["role"] == "subscriber"
    assert row["password_hash"] == f"hashed:{GOOD_PASSWORD}"  # went through the hasher


def test_email_is_stored_in_lowercase():
    service, users = make_service()
    service.register(RegisterRequest(email="Ann@Example.com", password=GOOD_PASSWORD))
    assert users.rows[0]["email"] == "ann@example.com"


def test_real_hasher_produces_an_argon2id_hash():
    users = FakeUserRepository()
    service = AuthService(users, Argon2PasswordHasher())
    service.register(RegisterRequest(phone="+250781000000", password=GOOD_PASSWORD))
    assert users.rows[0]["password_hash"].startswith("$argon2id$")


def test_taken_email_is_refused_even_with_different_case():
    service, _ = make_service()
    service.register(RegisterRequest(email="ann@example.com", password=GOOD_PASSWORD))
    with pytest.raises(ConflictError):
        service.register(RegisterRequest(email="ANN@example.com", password=GOOD_PASSWORD))


def test_taken_phone_is_refused():
    service, _ = make_service()
    service.register(RegisterRequest(phone="+250781000000", password=GOOD_PASSWORD))
    with pytest.raises(ConflictError):
        service.register(RegisterRequest(phone="+250781000000", password=GOOD_PASSWORD))


def test_password_must_be_at_least_12_characters():
    with pytest.raises(ValidationError):
        RegisterRequest(email="ann@example.com", password="short")


def test_password_has_a_maximum_length():
    with pytest.raises(ValidationError):
        RegisterRequest(email="ann@example.com", password="x" * 129)


def test_email_or_phone_is_required():
    with pytest.raises(ValidationError):
        RegisterRequest(password=GOOD_PASSWORD)


def test_bad_email_and_bad_phone_are_refused():
    with pytest.raises(ValidationError):
        RegisterRequest(email="not-an-email", password=GOOD_PASSWORD)
    with pytest.raises(ValidationError):
        RegisterRequest(phone="0781000000", password=GOOD_PASSWORD)


def test_unknown_fields_are_refused():
    with pytest.raises(ValidationError):
        RegisterRequest(email="ann@example.com", password=GOOD_PASSWORD, role="system_admin")


def test_password_is_hidden_when_printed():
    request = RegisterRequest(email="ann@example.com", password=GOOD_PASSWORD)
    assert GOOD_PASSWORD not in repr(request)