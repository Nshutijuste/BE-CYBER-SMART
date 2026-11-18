import uuid
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import LoginAttempt
from app.domain.entities import COUNTED_FAILURES, FailureWindow
from app.repositories._time import aware


class SqlLoginAttemptRepository:
    """Can add rows and count them. It cannot change or delete anything."""

    def __init__(self, session: Session) -> None:
        self._session = session

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
        self._session.add(
            LoginAttempt(
                attempted_at=at,
                user_id=user_id,
                identifier_hash=identifier_hash,
                source_ip=source_ip[:45],
                device_summary=device_summary[:200] if device_summary else None,
                success=success,
                failure_reason=failure_reason,
            )
        )
        self._session.commit()

    def failure_window(self, identifier_hash: str, since: datetime) -> FailureWindow:
        """Failures since the window began, or since the last success if that is later."""
        last_success = aware(
            self._session.scalar(
                select(func.max(LoginAttempt.attempted_at)).where(
                    LoginAttempt.identifier_hash == identifier_hash,
                    LoginAttempt.success.is_(True),
                    LoginAttempt.attempted_at >= since,
                )
            )
        )
        start = max(since, last_success) if last_success else since
        count, last = self._session.execute(
            select(func.count(), func.max(LoginAttempt.attempted_at)).where(
                LoginAttempt.identifier_hash == identifier_hash,
                LoginAttempt.failure_reason.in_(COUNTED_FAILURES),
                LoginAttempt.attempted_at > start,
            )
        ).one()
        return FailureWindow(count=count, last_at=aware(last))

    def failures_from_ip(self, source_ip: str, since: datetime) -> int:
        return self._session.scalar(
            select(func.count()).where(
                LoginAttempt.source_ip == source_ip[:45],
                LoginAttempt.failure_reason.in_(COUNTED_FAILURES),
                LoginAttempt.attempted_at > since,
            )
        )
