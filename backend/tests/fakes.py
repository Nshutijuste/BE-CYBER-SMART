import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from app.domain.entities import (
    COUNTED_FAILURES,
    FailureWindow,
    MfaState,
    RefreshTokenRecord,
    RefreshTokenRotationResult,
    UserCredentials,
    UserProfile,
)


class FakeClock:
    """A clock the test controls."""

    def __init__(self, start: datetime | None = None) -> None:
        self.now = start or datetime(2026, 11, 20, 12, 0, 0, tzinfo=UTC)

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kwargs: float) -> None:
        self.now += timedelta(**kwargs)


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

    def find_by_id(self, user_id: uuid.UUID) -> UserProfile | None:
        for row in self.rows:
            if row["id"] == user_id:
                return UserProfile(id=row["id"], role=row["role"], is_active=row["is_active"])
        return None

    def deactivate(self, user_id: uuid.UUID) -> None:
        self._row(user_id)["is_active"] = False

    def set_role(self, user_id: uuid.UUID, role: str) -> None:
        self._row(user_id)["role"] = role

    def _row(self, user_id: uuid.UUID) -> dict[str, Any]:
        return next(r for r in self.rows if r["id"] == user_id)


class FakeLoginAttemptRepository:
    """Keeps attempts in a list and counts them the same way the database version does."""

    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

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
    ) -> None:
        self.rows.append(
            {
                "user_id": user_id,
                "identifier_hash": identifier_hash,
                "source_ip": source_ip,
                "device_summary": device_summary,
                "success": success,
                "failure_reason": failure_reason,
                "at": at,
            }
        )

    def failure_window(self, identifier_hash: str, since: datetime) -> FailureWindow:
        mine = [r for r in self.rows if r["identifier_hash"] == identifier_hash]
        successes = [r["at"] for r in mine if r["success"] and r["at"] >= since]
        start = max([since, *successes])
        fails = [
            r["at"]
            for r in mine
            if r["failure_reason"] in COUNTED_FAILURES and r["at"] > start
        ]
        return FailureWindow(count=len(fails), last_at=max(fails) if fails else None)

    def failures_from_ip(self, source_ip: str, since: datetime) -> int:
        return sum(
            1
            for r in self.rows
            if r["source_ip"] == source_ip
            and r["failure_reason"] in COUNTED_FAILURES
            and r["at"] > since
        )


class FakeRefreshTokenRepository:
    def __init__(self) -> None:
        self.rows: dict[uuid.UUID, dict[str, Any]] = {}

    def add(
        self,
        *,
        user_id: uuid.UUID,
        family_id: uuid.UUID,
        token_hash: str,
        mfa_passed: bool,
        created_at: datetime,
        expires_at: datetime,
    ) -> None:
        token_id = uuid.uuid4()
        self.rows[token_id] = {
            "id": token_id,
            "user_id": user_id,
            "family_id": family_id,
            "token_hash": token_hash,
            "mfa_passed": mfa_passed,
            "expires_at": expires_at,
            "revoked_at": None,
        }

    def get_by_hash(self, token_hash: str) -> RefreshTokenRecord | None:
        for row in self.rows.values():
            if row["token_hash"] == token_hash:
                return self._record(row)
        return None

    def rotate(
        self,
        *,
        token_hash: str,
        replacement_hash: str,
        at: datetime,
        replacement_expires_at: datetime,
    ) -> RefreshTokenRotationResult:
        record = self.get_by_hash(token_hash)
        if record is None:
            return RefreshTokenRotationResult(record=None, replayed=False)
        if record.revoked_at is not None:
            self.revoke_family(record.family_id, at)
            return RefreshTokenRotationResult(record=record, replayed=True)
        if record.expires_at <= at:
            return RefreshTokenRotationResult(record=None, replayed=False)

        self.rows[record.id]["revoked_at"] = at
        self.add(
            user_id=record.user_id,
            family_id=record.family_id,
            token_hash=replacement_hash,
            mfa_passed=record.mfa_passed,
            created_at=at,
            expires_at=replacement_expires_at,
        )
        return RefreshTokenRotationResult(record=record, replayed=False)

    def revoke_family(self, family_id: uuid.UUID, at: datetime) -> None:
        for row in self.rows.values():
            if row["family_id"] == family_id and row["revoked_at"] is None:
                row["revoked_at"] = at

    def active_count(self) -> int:
        return sum(1 for r in self.rows.values() if r["revoked_at"] is None)

    @staticmethod
    def _record(row: dict[str, Any]) -> RefreshTokenRecord:
        return RefreshTokenRecord(
            id=row["id"],
            user_id=row["user_id"],
            family_id=row["family_id"],
            mfa_passed=row["mfa_passed"],
            expires_at=row["expires_at"],
            revoked_at=row["revoked_at"],
        )


class FakeMfaRepository:
    def __init__(self) -> None:
        self.rows: dict[uuid.UUID, dict[str, Any]] = {}
        self.reject_next_step = False
        self.reject_next_activation = False

    def get(self, user_id: uuid.UUID) -> MfaState | None:
        row = self.rows.get(user_id)
        if row is None:
            return None
        return MfaState(
            secret_encrypted=row["secret_encrypted"],
            enabled=row["enabled"],
            last_step=row["last_step"],
        )

    def save_pending(self, user_id: uuid.UUID, secret_encrypted: str, at: datetime) -> None:
        self.rows[user_id] = {
            "secret_encrypted": secret_encrypted,
            "enabled": False,
            "last_step": 0,
        }

    def activate(self, user_id: uuid.UUID, last_step: int) -> bool:
        if self.reject_next_activation:
            self.reject_next_activation = False
            return False
        row = self.rows[user_id]
        if row["enabled"] or row["last_step"] >= last_step:
            return False
        row["enabled"] = True
        row["last_step"] = last_step
        return True

    def record_step(self, user_id: uuid.UUID, last_step: int) -> bool:
        if self.reject_next_step:
            self.reject_next_step = False
            return False
        row = self.rows[user_id]
        if not row["enabled"] or row["last_step"] >= last_step:
            return False
        row["last_step"] = last_step
        return True


class FakeDeviceRepository:
    def __init__(self) -> None:
        self.rows: set[tuple[uuid.UUID, str]] = set()

    def touch(self, user_id: uuid.UUID, device_hash: str, at: datetime) -> bool:
        if (user_id, device_hash) in self.rows:
            return False
        had_any = any(u == user_id for u, _ in self.rows)
        self.rows.add((user_id, device_hash))
        return had_any


class FakeNotifier:
    def __init__(self) -> None:
        self.notices: list[dict[str, Any]] = []

    def new_device_login(
        self,
        *,
        user_id: uuid.UUID,
        device_summary: str | None,
        source_ip: str,
        at: datetime,
    ) -> None:
        self.notices.append(
            {"user_id": user_id, "device_summary": device_summary, "source_ip": source_ip}
        )


class FakeBreachChecker:
    def __init__(self, breached: set[str] | None = None) -> None:
        self.breached = breached or set()
        self.asked: list[str] = []

    def is_breached(self, password: str) -> bool:
        self.asked.append(password)
        return password in self.breached


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
