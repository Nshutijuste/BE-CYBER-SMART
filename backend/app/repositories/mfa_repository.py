import uuid
from datetime import datetime

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.db.models import MfaCredential
from app.domain.entities import MfaState


class SqlMfaRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, user_id: uuid.UUID) -> MfaState | None:
        row = self._session.get(MfaCredential, user_id)
        if row is None:
            return None
        return MfaState(
            secret_encrypted=row.secret_encrypted, enabled=row.enabled, last_step=row.last_step
        )

    def save_pending(self, user_id: uuid.UUID, secret_encrypted: str, at: datetime) -> None:
        row = self._session.get(MfaCredential, user_id)
        if row is None:
            self._session.add(
                MfaCredential(
                    user_id=user_id,
                    secret_encrypted=secret_encrypted,
                    enabled=False,
                    last_step=0,
                    created_at=at,
                )
            )
        else:
            row.secret_encrypted = secret_encrypted
            row.enabled = False
            row.last_step = 0
        self._session.commit()

    def activate(self, user_id: uuid.UUID, last_step: int) -> bool:
        result = self._session.execute(
            update(MfaCredential)
            .where(
                MfaCredential.user_id == user_id,
                MfaCredential.enabled.is_(False),
                MfaCredential.last_step < last_step,
            )
            .values(enabled=True, last_step=last_step)
        )
        self._session.commit()
        return result.rowcount == 1

    def record_step(self, user_id: uuid.UUID, last_step: int) -> bool:
        result = self._session.execute(
            update(MfaCredential)
            .where(
                MfaCredential.user_id == user_id,
                MfaCredential.enabled.is_(True),
                MfaCredential.last_step < last_step,
            )
            .values(last_step=last_step)
        )
        self._session.commit()
        return result.rowcount == 1
