import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from app.core.errors import AuthenticationError, TooManyAttemptsError
from app.domain.interfaces import (
    LoginAttemptRepository,
    MfaRepository,
    PasswordHasher,
    UserRepository,
)
from app.schemas.auth import LoginRequest
from app.services.throttle import Throttle

UNKNOWN_ACCOUNT = "unknown_account"
WRONG_PASSWORD = "wrong_password"
INACTIVE_ACCOUNT = "inactive_account"
THROTTLED = "throttled"


@dataclass(frozen=True)
class LoginOutcome:
    user_id: uuid.UUID
    needs_mfa: bool


def utc_now() -> datetime:
    return datetime.now(UTC)


class LoginService:
    def __init__(
        self,
        users: UserRepository,
        attempts: LoginAttemptRepository,
        mfa: MfaRepository,
        hasher: PasswordHasher,
        keyed_hash: Callable[[str], str],
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self._users = users
        self._attempts = attempts
        self._mfa = mfa
        self._hasher = hasher
        self._keyed_hash = keyed_hash
        self._clock = clock
        self._throttle = Throttle(attempts)

    def login(
        self,
        data: LoginRequest,
        *,
        source_ip: str,
        device_summary: str | None,
    ) -> LoginOutcome:
        now = self._clock()
        email = data.email.lower() if data.email else None
        password = data.password.get_secret_value()
        # The key is the typed identifier, whether or not an account exists, so a lockout
        # looks the same for real and invented accounts.
        key = self._keyed_hash(f"email:{email}" if email else f"phone:{data.phone}")

        wait = self._throttle.wait_seconds(key_hash=key, source_ip=source_ip, now=now)
        if wait > 0:
            self._record(None, key, source_ip, device_summary, THROTTLED, now)
            raise TooManyAttemptsError(wait)

        found = self._users.find_for_login(email=email, phone=data.phone)
        user_id: uuid.UUID | None = None
        failure: str | None = None
        if found is None:
            self._hasher.verify_dummy(password)  # same time as a real check
            failure = UNKNOWN_ACCOUNT
        else:
            user_id = found.id
            if not self._hasher.verify(found.password_hash, password):
                failure = WRONG_PASSWORD
            elif not found.is_active:
                failure = INACTIVE_ACCOUNT

        self._record(user_id, key, source_ip, device_summary, failure, now)
        if failure is not None or user_id is None:
            # One identical error for every failure. The reason stays in our records.
            raise AuthenticationError()

        state = self._mfa.get(user_id)
        return LoginOutcome(user_id=user_id, needs_mfa=bool(state and state.enabled))

    def _record(
        self,
        user_id: uuid.UUID | None,
        key: str,
        source_ip: str,
        device_summary: str | None,
        failure: str | None,
        now: datetime,
    ) -> None:
        self._attempts.record(
            user_id=user_id,
            identifier_hash=key,
            source_ip=source_ip,
            device_summary=device_summary,
            success=failure is None,
            failure_reason=failure,
            at=now,
        )
