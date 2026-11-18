import app.db.models  # noqa: F401
from app.db.base import Base


def test_all_tables_are_registered():
    expected = {
        "roles",
        "users",
        "login_attempts",
        "audit_entries",
        "refresh_tokens",
        "mfa_credentials",
        "known_devices",
    }
    assert expected <= set(Base.metadata.tables)
