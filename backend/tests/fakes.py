import uuid
from typing import Any


class FakeUserRepository:
    """In-memory stand-in for the real database repository."""

    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def email_exists(self, email: str) -> bool:
        return any(r["email"] == email for r in self.rows)

    def phone_exists(self, phone: str) -> bool:
        return any(r["phone"] == phone for r in self.rows)

    def add(
        self,
        *,
        email: str | None,
        phone: str | None,
        password_hash: str,
        role: str,
    ) -> uuid.UUID:
        user_id = uuid.uuid4()
        self.rows.append(
            {
                "id": user_id,
                "email": email,
                "phone": phone,
                "password_hash": password_hash,
                "role": role,
            }
        )
        return user_id


class FakePasswordHasher:
    """Fast, predictable hasher for tests that are not about hashing."""

    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password_hash: str, password: str) -> bool:
        return password_hash == f"hashed:{password}"

    def needs_rehash(self, password_hash: str) -> bool:
        return False