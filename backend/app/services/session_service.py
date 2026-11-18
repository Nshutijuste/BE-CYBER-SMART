import hashlib
import logging
import secrets
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.core.errors import InvalidSessionError
from app.core.tokens import TokenService
from app.domain.interfaces import (
    DeviceRepository,
    Notifier,
    RefreshTokenRepository,
    UserRepository,
)
from app.services.login_service import utc_now

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class IssuedSession:
    access_token: str
    refresh_token: str
    csrf_token: str


def hash_refresh_token(raw: str) -> str:
    """Only this hash is stored. A database leak does not hand out usable tokens."""
    return hashlib.sha256(raw.encode()).hexdigest()


class SessionService:
    def __init__(
        self,
        tokens: TokenService,
        refresh: RefreshTokenRepository,
        users: UserRepository,
        devices: DeviceRepository,
        notifier: Notifier,
        keyed_hash: Callable[[str], str],
        *,
        refresh_days: int = 14,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self._tokens = tokens
        self._refresh = refresh
        self._users = users
        self._devices = devices
        self._notifier = notifier
        self._keyed_hash = keyed_hash
        self._refresh_lifetime = timedelta(days=refresh_days)
        self._clock = clock

    def start(
        self,
        user_id: uuid.UUID,
        *,
        mfa_passed: bool,
        source_ip: str,
        device_summary: str | None,
    ) -> IssuedSession:
        now = self._clock()
        device_hash = self._keyed_hash(f"device:{device_summary or 'unknown'}")
        if self._devices.touch(user_id, device_hash, now):
            self._notifier.new_device_login(
                user_id=user_id, device_summary=device_summary, source_ip=source_ip, at=now
            )
        return self._issue(user_id, uuid.uuid4(), mfa_passed, now)

    def rotate(self, raw_refresh_token: str) -> IssuedSession:
        """Every use of a refresh token spends it and hands back a new one."""
        now = self._clock()
        record = self._refresh.get_by_hash(hash_refresh_token(raw_refresh_token))
        if record is None:
            raise InvalidSessionError()
        if record.revoked_at is not None:
            # A spent token came back: someone copied it. End the whole family.
            self._refresh.revoke_family(record.family_id, now)
            logger.warning("refresh_token_reuse family=%s", record.family_id)
            raise InvalidSessionError()
        if record.expires_at <= now:
            raise InvalidSessionError()
        profile = self._users.find_by_id(record.user_id)
        if profile is None or not profile.is_active:
            self._refresh.revoke_family(record.family_id, now)
            raise InvalidSessionError()

        self._refresh.revoke(record.id, now)
        return self._issue(record.user_id, record.family_id, record.mfa_passed, now)

    def end(self, raw_refresh_token: str) -> None:
        record = self._refresh.get_by_hash(hash_refresh_token(raw_refresh_token))
        if record is not None:
            self._refresh.revoke_family(record.family_id, self._clock())

    def _issue(
        self, user_id: uuid.UUID, family_id: uuid.UUID, mfa_passed: bool, now: datetime
    ) -> IssuedSession:
        raw = secrets.token_urlsafe(48)
        self._refresh.add(
            user_id=user_id,
            family_id=family_id,
            token_hash=hash_refresh_token(raw),
            mfa_passed=mfa_passed,
            created_at=now,
            expires_at=now + self._refresh_lifetime,
        )
        return IssuedSession(
            access_token=self._tokens.issue_access(user_id, mfa=mfa_passed),
            refresh_token=raw,
            csrf_token=secrets.token_urlsafe(32),
        )
