"""Prove that the DATABASE itself refuses to change the audit log.

Run from backend/ with (.venv) active and the database up:
    Linux / Git Bash:  PYTHONPATH=. python scripts/audit_rules_check.py
    PowerShell:        $env:PYTHONPATH="."; python scripts/audit_rules_check.py

Everything happens inside one transaction that is rolled back at the end,
so no data is left behind.
"""

import sys
import uuid

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from app.db.session import engine

INSERT = text(
    "INSERT INTO audit_entries (created_at, action, details, prev_hash, entry_hash) "
    "VALUES (now(), 'rules.check', '{}', :prev, :entry)"
)
results: list[bool] = []


def report(label: str, ok: bool, detail: str = "") -> None:
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {label}  {detail}")


def refused_with(conn, statement, params=None) -> str | None:
    """Run a statement. Return the database's complaint, or None if it was allowed."""
    savepoint = conn.begin_nested()
    try:
        conn.execute(statement, params or {})
    except DBAPIError as error:
        savepoint.rollback()
        return str(error.orig)
    savepoint.rollback()
    return None


def main() -> int:
    prev, entry = uuid.uuid4().hex + "0" * 32, uuid.uuid4().hex + "1" * 32
    with engine.connect() as conn:
        outer = conn.begin()
        conn.execute(INSERT, {"prev": prev, "entry": entry})
        report("adding an entry works", True)

        message = refused_with(conn, text("UPDATE audit_entries SET action = 'changed' WHERE entry_hash = :e"), {"e": entry})
        report("changing an entry is refused", message is not None and "append-only" in message)

        message = refused_with(conn, text("DELETE FROM audit_entries WHERE entry_hash = :e"), {"e": entry})
        report("deleting an entry is refused", message is not None and "append-only" in message)

        message = refused_with(conn, text("TRUNCATE audit_entries"))
        report("emptying the whole log is refused", message is not None and "append-only" in message)

        message = refused_with(conn, INSERT, {"prev": prev, "entry": uuid.uuid4().hex + "2" * 32})
        report("a second entry after the same entry (a fork) is refused", message is not None and "prev_hash" in message)

        outer.rollback()
    print(f"\n{sum(results)} of {len(results)} checks passed.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
