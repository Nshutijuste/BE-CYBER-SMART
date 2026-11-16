import uuid
from typing import Any

from app.domain.entities import UserCredentials


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
                "is_active": True,
            }
        )
        return user_id

    def find_for_login(
        self, *, email: str | None, phone: str | None
    ) -> UserCredentials | None:
        for row in self.rows:
            if (email is not None and row["email"] == email) or (
                phone is not None and row["phone"] == phone
            ):
                return UserCredentials(
                    id=row["id"],
                    password_hash=row["password_hash"],
                    is_active=row["is_active"],
                )
        return None

    def deactivate(self, user_id: uuid.UUID) -> None:
        for row in self.rows:
            if row["id"] == user_id:
                row["is_active"] = False


class FakeLoginAttemptRepository:
    """Keeps login attempts in a list so tests can read them."""

    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def record(
        self,
        *,
        user_id: uuid.UUID | None,
        source_ip: str,
        device_summary: str | None,
        success: bool,
        failure_reason: str | None,
    ) -> None:
        self.rows.append(
            {
                "user_id": user_id,
                "source_ip": source_ip,
                "device_summary": device_summary,
                "success": success,
                "failure_reason": failure_reason,
            }
        )


class FakePasswordHasher:
    """Fast, predictable hasher for tests that are not about hashing."""

    def __init__(self) -> None:
        self.dummy_calls = 0

    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password_hash: str, password: str) -> bool:
        return password_hash == f"hashed:{password}"

    def verify_dummy(self, password: str) -> None:
        self.dummy_calls += 1

    def needs_rehash(self, password_hash: str) -> bool:
        return False