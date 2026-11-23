import uuid
from dataclasses import replace
from datetime import UTC, datetime
from typing import Any

import pytest

from app.domain.audit import (
    GENESIS_HASH,
    AuditRecord,
    canonical_details,
    compute_entry_hash,
)
from app.services.audit_service import AuditService
from tests.fakes import FakeClock


class FakeAuditRepository:
    """Chains entries in memory the same way the database version does."""

    def __init__(self) -> None:
        self.rows: list[AuditRecord] = []

    def append(self, *, action, actor_user_id, details, created_at) -> AuditRecord:
        prev = self.rows[-1].entry_hash if self.rows else GENESIS_HASH
        record = AuditRecord(
            id=len(self.rows) + 1,
            created_at=created_at,
            actor_user_id=actor_user_id,
            action=action,
            details=details,
            prev_hash=prev,
            entry_hash=compute_entry_hash(
                prev_hash=prev,
                created_at=created_at,
                actor_user_id=actor_user_id,
                action=action,
                details=details,
            ),
        )
        self.rows.append(record)
        return record

    def all_entries(self) -> list[AuditRecord]:
        return list(self.rows)


@pytest.fixture
def world():
    repo = FakeAuditRepository()
    clock = FakeClock()
    return AuditService(repo, clock), repo, clock


def fill(service, clock, count=5):
    for number in range(count):
        clock.advance(seconds=1)
        service.record("login.succeeded", details={"number": number})


def test_the_first_entry_points_at_the_genesis_value(world):
    service, repo, _ = world
    service.record("account.created")
    assert repo.rows[0].prev_hash == GENESIS_HASH


def test_each_entry_holds_the_hash_of_the_one_before(world):
    service, repo, clock = world
    fill(service, clock, 3)
    assert repo.rows[1].prev_hash == repo.rows[0].entry_hash
    assert repo.rows[2].prev_hash == repo.rows[1].entry_hash


def test_an_untouched_log_verifies_and_an_empty_one_does_too(world):
    service, _, clock = world
    assert service.verify().ok is True
    fill(service, clock, 5)
    report = service.verify()
    assert (report.ok, report.checked) == (True, 5)


def test_a_changed_action_is_found(world):
    service, repo, clock = world
    fill(service, clock)
    repo.rows[2] = replace(repo.rows[2], action="login.failed")
    report = service.verify()
    assert (report.ok, report.broken_at, report.reason) == (False, 3, "entry_changed")


def test_changed_details_are_found(world):
    service, repo, clock = world
    fill(service, clock)
    repo.rows[1] = replace(repo.rows[1], details={"number": 999})
    assert service.verify().broken_at == 2


def test_a_deleted_entry_breaks_the_link(world):
    service, repo, clock = world
    fill(service, clock)
    del repo.rows[2]
    report = service.verify()
    assert (report.ok, report.broken_at, report.reason) == (False, 4, "link_broken")


def test_swapped_entries_are_found(world):
    service, repo, clock = world
    fill(service, clock)
    repo.rows[1], repo.rows[2] = repo.rows[2], repo.rows[1]
    assert service.verify().ok is False


def test_a_rewritten_entry_with_a_new_hash_still_breaks_the_next_link(world):
    service, repo, clock = world
    fill(service, clock)
    old = repo.rows[1]
    forged = replace(old, action="login.failed")
    forged = replace(
        forged,
        entry_hash=compute_entry_hash(
            prev_hash=forged.prev_hash,
            created_at=forged.created_at,
            actor_user_id=forged.actor_user_id,
            action=forged.action,
            details=forged.details,
        ),
    )
    repo.rows[1] = forged
    report = service.verify()
    assert (report.ok, report.broken_at, report.reason) == (False, 3, "link_broken")


def test_key_order_does_not_change_the_hash():
    assert canonical_details({"a": 1, "b": 2}) == canonical_details({"b": 2, "a": 1})


def test_a_naive_time_is_read_as_utc():
    when = datetime(2026, 1, 1, 12, 0, 0)
    same = when.replace(tzinfo=UTC)
    args: dict[str, Any] = {
        "prev_hash": GENESIS_HASH,
        "actor_user_id": None,
        "action": "a.b",
        "details": {},
    }
    assert compute_entry_hash(created_at=when, **args) == compute_entry_hash(created_at=same, **args)


def test_the_actor_is_part_of_the_hash():
    args: dict[str, Any] = {
        "prev_hash": GENESIS_HASH,
        "created_at": datetime(2026, 1, 1, tzinfo=UTC),
        "action": "a.b",
        "details": {},
    }
    assert compute_entry_hash(actor_user_id=uuid.uuid4(), **args) != compute_entry_hash(
        actor_user_id=uuid.uuid4(), **args
    )


@pytest.mark.parametrize(
    "key", ["password", "new_password", "refresh_token", "mfa_token", "secret", "code", "otp", "Authorization"]
)
def test_secrets_can_never_be_logged(world, key):
    service, repo, _ = world
    with pytest.raises(ValueError):
        service.record("login.failed", details={key: "x"})
    assert repo.rows == []


def test_harmless_keys_that_contain_the_word_code_are_fine(world):
    service, _, _ = world
    service.record("login.failed", details={"error_code": "wrong_password", "attempts": 3, "ok": False})


def test_nested_data_and_odd_types_are_refused(world):
    service, _, _ = world
    with pytest.raises(ValueError):
        service.record("a.b", details={"inner": {"x": 1}})
    with pytest.raises(ValueError):
        service.record("a.b", details={"items": [1, 2]})


@pytest.mark.parametrize("action", ["", "Login.Failed", "login failed", "login.", ".login", "x" * 101])
def test_actions_must_look_like_names(world, action):
    service, _, _ = world
    with pytest.raises(ValueError):
        service.record(action)


def test_long_text_is_cut_short(world):
    service, repo, _ = world
    service.record("login.failed", details={"device": "x" * 500})
    assert len(repo.rows[0].details["device"]) == 200
