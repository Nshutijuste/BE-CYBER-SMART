import uuid
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import KnownDevice


class SqlDeviceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def touch(self, user_id: uuid.UUID, device_hash: str, at: datetime) -> bool:
        known = self._session.scalar(
            select(KnownDevice).where(
                KnownDevice.user_id == user_id, KnownDevice.device_hash == device_hash
            )
        )
        if known is not None:
            known.last_seen_at = at
            self._session.commit()
            return False

        had_any = (
            self._session.scalar(
                select(func.count()).where(KnownDevice.user_id == user_id)
            )
            or 0
        ) > 0
        self._session.add(
            KnownDevice(
                user_id=user_id, device_hash=device_hash, first_seen_at=at, last_seen_at=at
            )
        )
        try:
            self._session.commit()
        except IntegrityError:  # two logins at the same moment: the other one won
            self._session.rollback()
            return False
        return had_any
