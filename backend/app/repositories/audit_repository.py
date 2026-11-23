import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db.models import AuditEntry
from app.domain.audit import GENESIS_HASH, AuditRecord, compute_entry_hash
from app.repositories._time import aware

AUDIT_LOCK_KEY = 7_204_001  # any fixed number: "only one writer at a time"


def _to_record(row: AuditEntry) -> AuditRecord:
    return AuditRecord(
        id=row.id,
        created_at=aware(row.created_at),
        actor_user_id=row.actor_user_id,
        action=row.action,
        details=row.details,
        prev_hash=row.prev_hash,
        entry_hash=row.entry_hash,
    )


class SqlAuditRepository:
    """Adds entries to the end of the chain and reads them. It never edits or deletes."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def append(
        self,
        *,
        action: str,
        actor_user_id: uuid.UUID | None,
        details: dict[str, Any],
        created_at: datetime,
    ) -> AuditRecord:
        if self._session.get_bind().dialect.name == "postgresql":
            # Two writers at the same moment would both extend the same entry and fork
            # the chain. This lock makes them take turns. It is released at commit.
            self._session.execute(
                text("SELECT pg_advisory_xact_lock(:key)"), {"key": AUDIT_LOCK_KEY}
            )
        last_hash = self._session.scalar(
            select(AuditEntry.entry_hash).order_by(AuditEntry.id.desc()).limit(1)
        )
        prev_hash = last_hash or GENESIS_HASH
        row = AuditEntry(
            created_at=created_at,
            actor_user_id=actor_user_id,
            action=action,
            details=details,
            prev_hash=prev_hash,
            entry_hash=compute_entry_hash(
                prev_hash=prev_hash,
                created_at=created_at,
                actor_user_id=actor_user_id,
                action=action,
                details=details,
            ),
        )
        self._session.add(row)
        self._session.commit()
        return _to_record(row)

    def all_entries(self) -> list[AuditRecord]:
        rows = self._session.scalars(select(AuditEntry).order_by(AuditEntry.id)).all()
        return [_to_record(row) for row in rows]
