from datetime import timedelta

from app.services.throttle import (
    IP_FAILURE_LIMIT,
    IP_RETRY_SECONDS,
    Throttle,
    lock_seconds,
    seconds_left,
)
from tests.fakes import FakeClock, FakeLoginAttemptRepository


def fail(attempts, clock, key="k1", ip="198.51.100.1", reason="wrong_password"):
    attempts.record(
        user_id=None,
        identifier_hash=key,
        source_ip=ip,
        device_summary=None,
        success=False,
        failure_reason=reason,
        at=clock.now,
    )


def test_lock_grows_after_five_free_failures_and_stops_at_fifteen_minutes():
    assert [lock_seconds(n) for n in (0, 4)] == [0, 0]
    assert [lock_seconds(n) for n in (5, 6, 7, 8)] == [30, 60, 120, 240]
    assert lock_seconds(10) == 900
    assert lock_seconds(500) == 900


def test_time_left_counts_down_and_never_goes_negative():
    clock = FakeClock()
    assert seconds_left(5, clock.now, clock.now) == 30
    assert seconds_left(5, clock.now, clock.now + timedelta(seconds=10)) == 20
    assert seconds_left(5, clock.now, clock.now + timedelta(seconds=999)) == 0
    assert seconds_left(5, None, clock.now) == 0


def test_four_failures_are_free():
    attempts, clock = FakeLoginAttemptRepository(), FakeClock()
    for _ in range(4):
        fail(attempts, clock)
    assert Throttle(attempts).wait_seconds(key_hash="k1", source_ip="x", now=clock.now) == 0


def test_the_fifth_failure_starts_a_wait_that_then_ends():
    attempts, clock = FakeLoginAttemptRepository(), FakeClock()
    throttle = Throttle(attempts)
    for _ in range(5):
        fail(attempts, clock)
    assert throttle.wait_seconds(key_hash="k1", source_ip="x", now=clock.now) == 30
    clock.advance(seconds=31)
    assert throttle.wait_seconds(key_hash="k1", source_ip="x", now=clock.now) == 0


def test_old_failures_leave_the_window():
    attempts, clock = FakeLoginAttemptRepository(), FakeClock()
    for _ in range(6):
        fail(attempts, clock)
    clock.advance(minutes=16)
    assert Throttle(attempts).wait_seconds(key_hash="k1", source_ip="x", now=clock.now) == 0


def test_a_success_clears_the_count():
    attempts, clock = FakeLoginAttemptRepository(), FakeClock()
    for _ in range(4):
        fail(attempts, clock)
    clock.advance(seconds=1)
    attempts.record(
        user_id=None, identifier_hash="k1", source_ip="x", device_summary=None,
        success=True, failure_reason=None, at=clock.now,
    )
    clock.advance(seconds=1)
    fail(attempts, clock)  # only one failure since the success
    assert Throttle(attempts).wait_seconds(key_hash="k1", source_ip="x", now=clock.now) == 0


def test_blocked_attempts_do_not_extend_the_wait():
    attempts, clock = FakeLoginAttemptRepository(), FakeClock()
    for _ in range(5):
        fail(attempts, clock)
    for _ in range(50):  # an attacker keeps knocking while locked
        fail(attempts, clock, reason="throttled")
    assert Throttle(attempts).wait_seconds(key_hash="k1", source_ip="x", now=clock.now) == 30


def test_one_address_failing_across_many_accounts_is_slowed_down():
    attempts, clock = FakeLoginAttemptRepository(), FakeClock()
    for number in range(IP_FAILURE_LIMIT):
        fail(attempts, clock, key=f"account-{number}", ip="203.0.113.9")
    throttle = Throttle(attempts)
    assert throttle.wait_seconds(
        key_hash="brand-new-account", source_ip="203.0.113.9", now=clock.now
    ) == IP_RETRY_SECONDS
    assert throttle.wait_seconds(
        key_hash="brand-new-account", source_ip="203.0.113.10", now=clock.now
    ) == 0
