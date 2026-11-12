from typing import Protocol


class PasswordHasher(Protocol):
    """What the rest of the app needs from a password hasher."""

    def hash(self, password: str) -> str: ...

    def verify(self, password_hash: str, password: str) -> bool: ...

    def needs_rehash(self, password_hash: str) -> bool: ...