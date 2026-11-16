import uuid
from typing import Protocol

from app.domain.entities import UserCredentials


class PasswordHasher(Protocol):
    """What the rest of the app needs from a password hasher."""

    def hash(self, password: str) -> str: ...

    def verify(self, password_hash: str, password: str) -> bool: ...

    def verify_dummy(self, password: str) -> None: ...

    def needs_rehash(self, password_hash: str) -> bool: ...


class UserRepository(Protocol):
    """What the rest of the app needs from user storage."""

    def email_exists(self, email: str) -> bool: ...

    def phone_exists(self, phone: str) -> bool: ...

    def add(
        self,
        *,
        email: str | None,
        phone: str | None,
        password_hash: str,
        role: str,
    ) -> uuid.UUID: ...

    def find_for_login(
        self, *, email: str | None, phone: str | None
    ) -> UserCredentials | None: ...


class LoginAttemptRepository(Protocol):
    """Where every login attempt is written down."""

    def record(
        self,
        *,
        user_id: uuid.UUID | None,
        source_ip: str,
        device_summary: str | None,
        success: bool,
        failure_reason: str | None,
    ) -> None: ...