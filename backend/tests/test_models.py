import app.db.models  # noqa: F401
from app.db.base import Base


def test_core_tables_are_registered():
    expected = {"roles", "users", "login_attempts", "audit_entries"}
    assert expected <= set(Base.metadata.tables)