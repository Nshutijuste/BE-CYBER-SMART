import uuid

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.models import LoginAttempt, Role, User
from app.repositories.login_attempt_repository import SqlLoginAttemptRepository
from app.repositories.user_repository import SqlUserRepository


@pytest.fixture
def db():
    engine = create_engine("sqlite://")
    tables = [Role.__table__, User.__table__, LoginAttempt.__table__]
    Base.metadata.create_all(engine, tables=tables)
    with Session(engine) as session:
        session.add(Role(name="subscriber"))
        session.commit()
        yield session
    engine.dispose()


def test_find_for_login_by_email_and_by_phone(db):
    repo = SqlUserRepository(db)
    user_id = repo.add(
        email="ann@example.com", phone="+250781000000", password_hash="h", role="subscriber"
    )
    by_email = repo.find_for_login(email="ann@example.com", phone=None)
    by_phone = repo.find_for_login(email=None, phone="+250781000000")
    assert by_email.id == by_phone.id == user_id
    assert by_email.password_hash == "h"
    assert by_email.is_active is True


def test_find_for_login_returns_nothing_for_unknown_details(db):
    repo = SqlUserRepository(db)
    assert repo.find_for_login(email="nobody@example.com", phone=None) is None
    assert repo.find_for_login(email=None, phone=None) is None


def test_record_writes_a_success_and_a_failure_without_a_user(db):
    attempts = SqlLoginAttemptRepository(db)
    attempts.record(
        user_id=None,
        source_ip="203.0.113.7",
        device_summary="Browser/1",
        success=False,
        failure_reason="unknown_account",
    )
    user_id = SqlUserRepository(db).add(
        email="ann@example.com", phone=None, password_hash="h", role="subscriber"
    )
    attempts.record(
        user_id=user_id,
        source_ip="203.0.113.7",
        device_summary=None,
        success=True,
        failure_reason=None,
    )
    rows = db.scalars(select(LoginAttempt).order_by(LoginAttempt.id)).all()
    assert [r.success for r in rows] == [False, True]
    assert rows[0].user_id is None
    assert rows[0].failure_reason == "unknown_account"
    assert isinstance(rows[1].user_id, uuid.UUID)
    assert rows[1].attempted_at is not None
