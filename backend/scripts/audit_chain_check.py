"""Check that the audit log has not been changed.

Run from backend/ with (.venv) active and the database up:
    Linux / Git Bash:  PYTHONPATH=. python scripts/audit_chain_check.py
    PowerShell:        $env:PYTHONPATH="."; python scripts/audit_chain_check.py

Add --demo to write three demo entries first.
Exit code 0 means the log is intact, 1 means it was changed.
"""

import sys

from app.db.session import SessionLocal
from app.repositories.audit_repository import SqlAuditRepository
from app.services.audit_service import AuditService


def main() -> int:
    with SessionLocal() as session:
        service = AuditService(SqlAuditRepository(session))
        if "--demo" in sys.argv:
            service.record("demo.started", details={"note": "first demo entry"})
            service.record("demo.step", details={"number": 2})
            service.record("demo.finished", details={"done": True})
        report = service.verify()
    if report.ok:
        print(f"INTACT: {report.checked} entries, every link and hash matches.")
        return 0
    print(f"CHANGED: the log breaks at entry {report.broken_at} ({report.reason}).")
    print(f"{report.checked} entries before it were fine.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
