import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.models import AuditEntry
from app.domain.audit import GENESIS_HASH
from app.repositories.audit_repository import SqlAuditRepository
from app.services.audit_service import AuditService


@pytest.fixture
def db():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine, tables=[AuditEntry.__table__])
    with Session(engine) as session:
        yield session
    engine.dispose()


def test_entries_are_chained_and_read_back_in_order(db):
    service = AuditService(SqlAuditRepository(db))
    first = service.record("account.created", actor_user_id=uuid.uuid4(), details={"via": "web"})
    second = service.record("login.succeeded")
    rows = SqlAuditRepository(db).all_entries()
    assert [r.id for r in rows] == [first.id, second.id]
    assert rows[0].prev_hash == GENESIS_HASH
    assert rows[1].prev_hash == rows[0].entry_hash
    assert rows[0].created_at.tzinfo is not None
    assert rows[0].details == {"via": "web"}


def test_the_real_database_round_trip_still_verifies(db):
    service = AuditService(SqlAuditRepository(db))
    for number in range(5):
        service.record("login.failed", details={"number": number, "reason": "wrong_password"})
    report = service.verify()
    assert (report.ok, report.checked) == (True, 5)


def test_changing_a_stored_row_is_detected(db):
    service = AuditService(SqlAuditRepository(db))
    for _ in range(4):
        service.record("login.succeeded")
    db.execute(text("UPDATE audit_entries SET action = 'login.failed' WHERE id = 2"))
    db.commit()
    report = service.verify()
    assert (report.ok, report.broken_at, report.reason) == (False, 2, "entry_changed")


def test_deleting_a_stored_row_is_detected(db):
    service = AuditService(SqlAuditRepository(db))
    for _ in range(4):
        service.record("login.succeeded")
    db.execute(text("DELETE FROM audit_entries WHERE id = 2"))
    db.commit()
    assert service.verify().reason == "link_broken"


def test_a_stored_time_without_a_zone_is_read_as_utc(db):
    AuditService(SqlAuditRepository(db), clock=lambda: datetime(2026, 5, 5, tzinfo=UTC)).record("a.b")
    assert SqlAuditRepository(db).all_entries()[0].created_at == datetime(2026, 5, 5, tzinfo=UTC)
