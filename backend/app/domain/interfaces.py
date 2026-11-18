import uuid
from datetime import datetime
from typing import Protocol

from app.domain.entities import (
    FailureWindow,
    MfaState,
    RefreshTokenRecord,
    UserCredentials,
    UserProfile,
)


class PasswordHasher(Protocol):
    """What the rest of the app needs from a password hasher."""

    def hash(self, password: str) -> str: ...

    def verify(self, password_hash: str, password: str) -> bool: ...

    def verify_dummy(self, password: str) -> None: ...

    def needs_rehash(self, password_hash: str) -> bool: ...


class BreachChecker(Protocol):
    def is_breached(self, password: str) -> bool: ...


class Notifier(Protocol):
    def new_device_login(
        self,
        *,
        user_id: uuid.UUID,
        device_summary: str | None,
        source_ip: str,
        at: datetime,
    ) -> None: ...


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

    def find_by_id(self, user_id: uuid.UUID) -> UserProfile | None: ...


class LoginAttemptRepository(Protocol):
    """Where every login attempt is written down."""

    def record(
        self,
        *,
        user_id: uuid.UUID | None,
        identifier_hash: str | None,
        source_ip: str,
        device_summary: str | None,
        success: bool,
        failure_reason: str | None,
        at: datetime,
    ) -> None: ...

    def failure_window(self, identifier_hash: str, since: datetime) -> FailureWindow: ...

    def failures_from_ip(self, source_ip: str, since: datetime) -> int: ...


class RefreshTokenRepository(Protocol):
    def add(
        self,
        *,
        user_id: uuid.UUID,
        family_id: uuid.UUID,
        token_hash: str,
        mfa_passed: bool,
        created_at: datetime,
        expires_at: datetime,
    ) -> None: ...

    def get_by_hash(self, token_hash: str) -> RefreshTokenRecord | None: ...

    def revoke(self, token_id: uuid.UUID, at: datetime) -> None: ...

    def revoke_family(self, family_id: uuid.UUID, at: datetime) -> None: ...


class MfaRepository(Protocol):
    def get(self, user_id: uuid.UUID) -> MfaState | None: ...

    def save_pending(self, user_id: uuid.UUID, secret_encrypted: str, at: datetime) -> None: ...

    def activate(self, user_id: uuid.UUID, last_step: int) -> None: ...

    def record_step(self, user_id: uuid.UUID, last_step: int) -> None: ...


class DeviceRepository(Protocol):
    def touch(self, user_id: uuid.UUID, device_hash: str, at: datetime) -> bool:
        """Remember this device. True only if it is NEW for a user who had others."""
        ...
