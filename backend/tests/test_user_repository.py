import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.errors import ConflictError
from app.db.base import Base
from app.db.models import Role, User
from app.repositories.user_repository import SqlUserRepository


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    # Only the tables this repository needs (the audit table uses Postgres-only types).
    Base.metadata.create_all(engine, tables=[Role.__table__, User.__table__])
    with Session(engine) as db:
        db.add(Role(name="subscriber"))
        db.commit()
        yield db
    engine.dispose()


def test_add_saves_a_user_with_the_right_role(session):
    repo = SqlUserRepository(session)
    user_id = repo.add(email="ann@example.com", phone=None, password_hash="h", role="subscriber")
    user = session.scalar(select(User).where(User.id == user_id))
    assert user.email == "ann@example.com"
    assert user.password_hash == "h"
    assert user.role.name == "subscriber"


def test_exists_checks(session):
    repo = SqlUserRepository(session)
    repo.add(email="ann@example.com", phone="+250781000000", password_hash="h", role="subscriber")
    assert repo.email_exists("ann@example.com") is True
    assert repo.email_exists("bob@example.com") is False
    assert repo.phone_exists("+250781000000") is True
    assert repo.phone_exists("+250781999999") is False


def test_a_duplicate_that_slips_past_the_check_becomes_a_conflict(session):
    repo = SqlUserRepository(session)
    repo.add(email="ann@example.com", phone=None, password_hash="h", role="subscriber")
    with pytest.raises(ConflictError):
        repo.add(email="ann@example.com", phone=None, password_hash="h", role="subscriber")


def test_a_missing_role_is_a_server_problem_not_a_user_error(session):
    repo = SqlUserRepository(session)
    with pytest.raises(RuntimeError):
        repo.add(email="ann@example.com", phone=None, password_hash="h", role="nonexistent")