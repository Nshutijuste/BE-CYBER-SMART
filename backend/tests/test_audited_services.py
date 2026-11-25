import uuid
from types import SimpleNamespace

import pytest

from app.core.errors import AuthenticationError, TooManyAttemptsError
from app.services.audited import (
    AuditedLoginService,
    AuditedMfaService,
    AuditedSessionService,
)

USER = uuid.uuid4()
IP = "203.0.113.7"


class RecordingAudit:
    def __init__(self) -> None:
        self.events: list[tuple[str, uuid.UUID | None, dict]] = []

    def record(self, action, *, actor_user_id=None, details=None):
        self.events.append((action, actor_user_id, details or {}))


class BrokenAudit:
    def record(self, action, *, actor_user_id=None, details=None):
        raise RuntimeError("the audit table is down")


class StubLogin:
    def __init__(self, error=None, needs_mfa=False):
        self.error, self.needs_mfa = error, needs_mfa

    def login(self, data, *, source_ip, device_summary):
        if self.error:
            raise self.error
        return SimpleNamespace(user_id=USER, needs_mfa=self.needs_mfa)


class StubSession:
    def start(self, user_id, **kwargs):
        return "issued"

    def rotate(self, raw):
        return "rotated"

    def end(self, raw):
        return None


class StubMfa:
    def __init__(self, error=None):
        self.error = error

    def begin_setup(self, user_id, label):
        return "setup"

    def confirm_setup(self, user_id, code, *, source_ip):
        if self.error:
            raise self.error

    def verify_login_code(self, user_id, code, *, source_ip):
        if self.error:
            raise self.error


def login(service):
    return service.login(object(), source_ip=IP, device_summary="Browser/1")


def test_a_good_password_is_written_with_who_and_from_where():
    audit = RecordingAudit()
    outcome = login(AuditedLoginService(StubLogin(needs_mfa=True), audit))
    assert outcome.user_id == USER
    assert audit.events == [
        ("login.password_ok", USER, {"ip": IP, "second_step_needed": True})
    ]


def test_a_failed_login_is_written_without_a_person_and_still_fails():
    audit = RecordingAudit()
    with pytest.raises(AuthenticationError):
        login(AuditedLoginService(StubLogin(error=AuthenticationError()), audit))
    assert audit.events == [("login.failed", None, {"ip": IP})]


def test_a_lockout_is_not_written_one_by_one():
    audit = RecordingAudit()
    with pytest.raises(TooManyAttemptsError):
        login(AuditedLoginService(StubLogin(error=TooManyAttemptsError(30)), audit))
    assert audit.events == []


def test_a_broken_audit_log_never_breaks_a_login():
    assert login(AuditedLoginService(StubLogin(), BrokenAudit())).user_id == USER
    with pytest.raises(AuthenticationError):  # the user still sees the real error
        login(AuditedLoginService(StubLogin(error=AuthenticationError()), BrokenAudit()))


def test_a_started_session_is_written_with_the_second_step_flag():
    audit = RecordingAudit()
    service = AuditedSessionService(StubSession(), audit)
    assert service.start(USER, mfa_passed=True, source_ip=IP, device_summary=None) == "issued"
    assert audit.events == [("session.started", USER, {"ip": IP, "second_step": True})]


def test_refreshing_and_ending_a_session_pass_straight_through():
    audit = RecordingAudit()
    service = AuditedSessionService(StubSession(), audit)
    assert service.rotate("token") == "rotated"
    assert service.end("token") is None
    assert audit.events == []


def test_second_step_setup_and_confirmation_are_written():
    audit = RecordingAudit()
    service = AuditedMfaService(StubMfa(), audit)
    assert service.begin_setup(USER, "label") == "setup"
    service.confirm_setup(USER, "123456", source_ip=IP)
    assert [e[0] for e in audit.events] == ["mfa.setup_started", "mfa.enabled"]
    assert audit.events[1][2] == {"ip": IP}


def test_a_wrong_second_step_code_is_written_and_still_fails():
    audit = RecordingAudit()
    with pytest.raises(AuthenticationError):
        AuditedMfaService(StubMfa(error=AuthenticationError()), audit).verify_login_code(
            USER, "000000", source_ip=IP
        )
    with pytest.raises(AuthenticationError):
        AuditedMfaService(StubMfa(error=AuthenticationError()), audit).confirm_setup(
            USER, "000000", source_ip=IP
        )
    assert [e[0] for e in audit.events] == ["mfa.failed", "mfa.confirm_failed"]


def test_a_good_second_step_code_is_written_and_a_lockout_is_not():
    audit = RecordingAudit()
    AuditedMfaService(StubMfa(), audit).verify_login_code(USER, "123456", source_ip=IP)
    with pytest.raises(TooManyAttemptsError):
        AuditedMfaService(StubMfa(error=TooManyAttemptsError(30)), audit).verify_login_code(
            USER, "000000", source_ip=IP
        )
    assert [e[0] for e in audit.events] == ["mfa.verified"]


def test_no_event_ever_carries_a_password_or_a_code():
    audit = RecordingAudit()
    login(AuditedLoginService(StubLogin(), audit))
    AuditedMfaService(StubMfa(), audit).verify_login_code(USER, "123456", source_ip=IP)
    for _, _, details in audit.events:
        assert not any(w in key for key in details for w in ("password", "token", "code", "secret"))
