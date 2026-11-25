"""Adds audit entries around the services. The services themselves stay untouched."""

import logging
import uuid
from typing import Any

from app.core.errors import AuthenticationError
from app.services.audit_service import AuditService

logger = logging.getLogger(__name__)


class _Audited:
    def __init__(self, inner: Any, audit: AuditService) -> None:
        self._inner = inner
        self._audit = audit

    def _note(self, action: str, actor: uuid.UUID | None = None, **details: Any) -> None:
        """A failed audit write must never break a login. It is logged loudly instead."""
        try:
            self._audit.record(action, actor_user_id=actor, details=details)
        except Exception:
            logger.exception("audit_write_failed action=%s", action)


class AuditedLoginService(_Audited):
    def login(self, data: Any, *, source_ip: str, device_summary: str | None) -> Any:
        try:
            outcome = self._inner.login(data, source_ip=source_ip, device_summary=device_summary)
        except AuthenticationError:
            # Lockouts (TooManyAttemptsError) are not written here one by one:
            # an attacker could fill the log. The attempts table already holds them.
            self._note("login.failed", ip=source_ip)
            raise
        self._note(
            "login.password_ok",
            outcome.user_id,
            ip=source_ip,
            second_step_needed=outcome.needs_mfa,
        )
        return outcome


class AuditedSessionService(_Audited):
    def start(self, user_id: uuid.UUID, **kwargs: Any) -> Any:
        issued = self._inner.start(user_id, **kwargs)
        self._note(
            "session.started",
            user_id,
            ip=kwargs.get("source_ip", "unknown"),
            second_step=bool(kwargs.get("mfa_passed")),
        )
        return issued

    def rotate(self, raw_refresh_token: str) -> Any:
        return self._inner.rotate(raw_refresh_token)

    def end(self, raw_refresh_token: str) -> None:
        self._inner.end(raw_refresh_token)


class AuditedMfaService(_Audited):
    def begin_setup(self, user_id: uuid.UUID, *args: Any, **kwargs: Any) -> Any:
        result = self._inner.begin_setup(user_id, *args, **kwargs)
        self._note("mfa.setup_started", user_id)
        return result

    def confirm_setup(self, user_id: uuid.UUID, *args: Any, **kwargs: Any) -> None:
        ip = kwargs.get("source_ip", "unknown")
        try:
            self._inner.confirm_setup(user_id, *args, **kwargs)
        except AuthenticationError:
            self._note("mfa.confirm_failed", user_id, ip=ip)
            raise
        self._note("mfa.enabled", user_id, ip=ip)

    def verify_login_code(self, user_id: uuid.UUID, *args: Any, **kwargs: Any) -> None:
        ip = kwargs.get("source_ip", "unknown")
        try:
            self._inner.verify_login_code(user_id, *args, **kwargs)
        except AuthenticationError:
            self._note("mfa.failed", user_id, ip=ip)
            raise
        self._note("mfa.verified", user_id, ip=ip)
