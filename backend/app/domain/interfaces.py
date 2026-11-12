import uuid
from typing import Protocol


class PasswordHasher(Protocol):
    """What the rest of the app needs from a password hasher."""

    def hash(self, password: str) -> str: ...

    def verify(self, password_hash: str, password: str) -> bool: ...

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