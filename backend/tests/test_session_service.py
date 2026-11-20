import hashlib
import uuid

import pytest

from app.core.crypto import KeyedHasher
from app.core.errors import InvalidSessionError
from app.core.tokens import TokenService
from app.services.session_service import SessionService
from tests.fakes import (
    FakeClock,
    FakeDeviceRepository,
    FakeNotifier,
    FakeRefreshTokenRepository,
    FakeUserRepository,
)

SECRET = "a-test-secret-long-enough"
IP = "203.0.113.7"


@pytest.fixture
def world():
    tokens = TokenService(SECRET)
    refresh = FakeRefreshTokenRepository()
    users = FakeUserRepository()
    devices = FakeDeviceRepository()
    notifier = FakeNotifier()
    clock = FakeClock()
    service = SessionService(
        tokens, refresh, users, devices, notifier, KeyedHasher(SECRET), refresh_days=14, clock=clock
    )
    user_id = users.add(email="ann@example.com", phone=None, password_hash="h", role="subscriber")
    return service, tokens, refresh, users, notifier, clock, user_id


def start(service, user_id, device="Phone/1", mfa=False):
    return service.start(user_id, mfa_passed=mfa, source_ip=IP, device_summary=device)


def test_start_gives_a_working_access_token(world):
    service, tokens, *_, user_id = world
    issued = start(service, user_id, mfa=True)
    claims = tokens.decode_access(issued.access_token)
    assert (claims.user_id, claims.mfa) == (user_id, True)
    assert issued.csrf_token and issued.refresh_token


def test_only_a_hash_of_the_refresh_token_is_stored(world):
    service, _, refresh, *_, user_id = world
    issued = start(service, user_id)
    stored = next(iter(refresh.rows.values()))["token_hash"]
    assert stored == hashlib.sha256(issued.refresh_token.encode()).hexdigest()
    assert issued.refresh_token not in str(refresh.rows)


def test_the_first_device_sends_no_notice_but_a_new_one_does(world):
    service, _, _, _, notifier, _, user_id = world
    start(service, user_id, device="Phone/1")
    assert notifier.notices == []
    start(service, user_id, device="Phone/1")  # same device again
    assert notifier.notices == []
    start(service, user_id, device="Laptop/2")  # a new one
    assert len(notifier.notices) == 1
    assert notifier.notices[0]["device_summary"] == "Laptop/2"
    assert notifier.notices[0]["user_id"] == user_id


def test_rotating_spends_the_old_token_and_keeps_the_second_step_flag(world):
    service, tokens, refresh, *_, user_id = world
    first = start(service, user_id, mfa=True)
    second = service.rotate(first.refresh_token)
    assert second.refresh_token != first.refresh_token
    assert refresh.active_count() == 1
    assert tokens.decode_access(second.access_token).mfa is True


def test_a_spent_token_that_comes_back_ends_the_whole_family(world):
    service, _, refresh, *_, user_id = world
    first = start(service, user_id)
    second = service.rotate(first.refresh_token)
    with pytest.raises(InvalidSessionError):
        service.rotate(first.refresh_token)  # replay of the stolen, spent token
    assert refresh.active_count() == 0
    with pytest.raises(InvalidSessionError):
        service.rotate(second.refresh_token)  # the new one is dead too


def test_a_replay_detected_during_atomic_rotation_ends_the_family(world, monkeypatch):
    service, _, refresh, *_, user_id = world
    first = start(service, user_id)
    rotate = refresh.rotate

    def competing_rotation(**kwargs):
        winner = rotate(
            **{
                **kwargs,
                "replacement_hash": "concurrent-successor-hash",
            }
        )
        assert winner.record is not None
        return rotate(
            **{
                **kwargs,
                "replacement_hash": "replayed-successor-hash",
            }
        )

    monkeypatch.setattr(refresh, "rotate", competing_rotation)
    with pytest.raises(InvalidSessionError):
        service.rotate(first.refresh_token)
    assert refresh.active_count() == 0


def test_an_unknown_token_is_refused(world):
    service, *_ = world
    with pytest.raises(InvalidSessionError):
        service.rotate("not-a-real-token")


def test_an_expired_token_is_refused(world):
    service, _, _, _, _, clock, user_id = world
    issued = start(service, user_id)
    clock.advance(days=15)
    with pytest.raises(InvalidSessionError):
        service.rotate(issued.refresh_token)


def test_a_deactivated_user_cannot_refresh(world):
    service, _, refresh, users, _, _, user_id = world
    issued = start(service, user_id)
    users.deactivate(user_id)
    with pytest.raises(InvalidSessionError):
        service.rotate(issued.refresh_token)
    assert refresh.active_count() == 0


def test_a_removed_user_cannot_refresh(world):
    service, _, _, users, _, _, user_id = world
    issued = start(service, user_id)
    users.rows.clear()
    with pytest.raises(InvalidSessionError):
        service.rotate(issued.refresh_token)


def test_ending_a_session_kills_its_refresh_tokens(world):
    service, _, refresh, *_, user_id = world
    issued = start(service, user_id)
    service.end(issued.refresh_token)
    assert refresh.active_count() == 0
    service.end("unknown-token")  # ending nothing is not an error
    assert isinstance(user_id, uuid.UUID)
