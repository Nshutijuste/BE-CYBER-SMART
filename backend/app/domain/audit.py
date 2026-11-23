"""A tamper-evident log: every entry holds the hash of the entry before it."""

import hashlib
import json
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

GENESIS_HASH = "0" * 64  # what "the entry before the first one" looks like


@dataclass(frozen=True)
class AuditRecord:
    id: int
    created_at: datetime
    actor_user_id: uuid.UUID | None
    action: str
    details: dict[str, Any]
    prev_hash: str
    entry_hash: str


@dataclass(frozen=True)
class ChainReport:
    ok: bool
    checked: int
    broken_at: int | None = None
    reason: str | None = None


class AuditRepository(Protocol):
    def append(
        self,
        *,
        action: str,
        actor_user_id: uuid.UUID | None,
        details: dict[str, Any],
        created_at: datetime,
    ) -> AuditRecord: ...

    def all_entries(self) -> list[AuditRecord]: ...


def canonical_details(details: dict[str, Any]) -> str:
    """The same details always give the same text, whatever order the keys came in."""
    return json.dumps(details, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_entry_hash(
    *,
    prev_hash: str,
    created_at: datetime,
    actor_user_id: uuid.UUID | None,
    action: str,
    details: dict[str, Any],
) -> str:
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)
    # A list of fields, so one field can never be mistaken for another.
    material = json.dumps(
        [
            prev_hash,
            created_at.astimezone(UTC).isoformat(timespec="microseconds"),
            str(actor_user_id) if actor_user_id else "",
            action,
            canonical_details(details),
        ],
        separators=(",", ":"),
    )
    return hashlib.sha256(material.encode()).hexdigest()


def verify_chain(records: Iterable[AuditRecord]) -> ChainReport:
    """Walk the log from the start. Report the first entry that does not fit."""
    expected_prev = GENESIS_HASH
    checked = 0
    for record in records:
        if record.prev_hash != expected_prev:
            return ChainReport(False, checked, record.id, "link_broken")
        recomputed = compute_entry_hash(
            prev_hash=record.prev_hash,
            created_at=record.created_at,
            actor_user_id=record.actor_user_id,
            action=record.action,
            details=record.details,
        )
        if record.entry_hash != recomputed:
            return ChainReport(False, checked, record.id, "entry_changed")
        expected_prev = record.entry_hash
        checked += 1
    return ChainReport(True, checked)
