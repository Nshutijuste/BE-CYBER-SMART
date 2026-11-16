import uuid

from sqlalchemy.orm import Session

from app.db.models import LoginAttempt


class SqlLoginAttemptRepository:
    """Append-only: this class can add rows and nothing else."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def record(
        self,
        *,
        user_id: uuid.UUID | None,
        source_ip: str,
        device_summary: str | None,
        success: bool,
        failure_reason: str | None,
    ) -> None:
        self._session.add(
            LoginAttempt(
                user_id=user_id,
                source_ip=source_ip[:45],
                device_summary=device_summary[:200] if device_summary else None,
                success=success,
                failure_reason=failure_reason,
            )
        )
        self._session.commit()
