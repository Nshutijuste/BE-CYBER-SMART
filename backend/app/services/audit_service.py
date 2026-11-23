import re
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from app.domain.audit import AuditRecord, AuditRepository, ChainReport, verify_chain

ACTION_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")  # e.g. login.failed
MAX_TEXT = 200
_FORBIDDEN_EXACT = {"code", "otp", "authorization", "cookie"}
_FORBIDDEN_PARTS = ("password", "token", "secret")


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _is_forbidden(key: str) -> bool:
    lowered = key.lower()
    return lowered in _FORBIDDEN_EXACT or any(part in lowered for part in _FORBIDDEN_PARTS)


def _clean(details: dict[str, Any] | None) -> dict[str, Any]:
    """Only plain facts go in the log: never secrets, never nested data."""
    clean: dict[str, Any] = {}
    for key, value in (details or {}).items():
        if _is_forbidden(key):
            raise ValueError(f"'{key}' must never be written to the audit log")
        if isinstance(value, str):
            clean[key] = value[:MAX_TEXT]
        elif value is None or isinstance(value, bool | int):
            clean[key] = value
        else:
            raise ValueError(f"'{key}' must be text, a number, true/false or empty")
    return clean


class AuditService:
    def __init__(
        self,
        entries: AuditRepository,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        self._entries = entries
        self._clock = clock

    def record(
        self,
        action: str,
        *,
        actor_user_id: uuid.UUID | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditRecord:
        if not ACTION_PATTERN.match(action) or len(action) > 100:
            raise ValueError("action must look like 'login.failed'")
        return self._entries.append(
            action=action,
            actor_user_id=actor_user_id,
            details=_clean(details),
            created_at=self._clock(),
        )

    def verify(self) -> ChainReport:
        return verify_chain(self._entries.all_entries())
