import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from app.core.crypto import FieldCipher
from app.core.errors import (
    AuthenticationError,
    MfaAlreadyEnabledError,
    TooManyAttemptsError,
)
from app.core.totp import new_secret, provisioning_uri, verify_totp
from app.domain.interfaces import LoginAttemptRepository, MfaRepository
from app.services.login_service import utc_now
from app.services.throttle import Throttle

MFA_FAILED = "mfa_failed"
THROTTLED = "throttled"


@dataclass(frozen=True)
class MfaSetup:
    secret: str
    otpauth_uri: str


class MfaService:
    def __init__(
        self,
        mfa: MfaRepository,
        attempts: LoginAttemptRepository,
        cipher: FieldCipher,
        keyed_hash: Callable[[str], str],
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self._mfa = mfa
        self._attempts = attempts
        self._cipher = cipher
        self._keyed_hash = keyed_hash
        self._clock = clock
        self._throttle = Throttle(attempts)

    def begin_setup(self, user_id: uuid.UUID, account_label: str) -> MfaSetup:
        state = self._mfa.get(user_id)
        if state is not None and state.enabled:
            raise MfaAlreadyEnabledError()
        secret = new_secret()
        sealed = self._cipher.encrypt(secret, aad=str(user_id).encode())
        self._mfa.save_pending(user_id, sealed, self._clock())
        return MfaSetup(secret=secret, otpauth_uri=provisioning_uri(secret, account_label))

    def confirm_setup(self, user_id: uuid.UUID, code: str, *, source_ip: str) -> None:
        state = self._mfa.get(user_id)
        if state is None or state.enabled:
            raise AuthenticationError()
        step = self._check(user_id, state.secret_encrypted, state.last_step, code, source_ip)
        self._mfa.activate(user_id, step)

    def verify_login_code(self, user_id: uuid.UUID, code: str, *, source_ip: str) -> None:
        state = self._mfa.get(user_id)
        if state is None or not state.enabled:
            raise AuthenticationError()
        step = self._check(user_id, state.secret_encrypted, state.last_step, code, source_ip)
        self._mfa.record_step(user_id, step)

    def _check(
        self,
        user_id: uuid.UUID,
        secret_encrypted: str,
        last_step: int,
        code: str,
        source_ip: str,
    ) -> int:
        now = self._clock()
        key = self._keyed_hash(f"mfa:{user_id}")
        wait = self._throttle.wait_seconds(key_hash=key, source_ip=source_ip, now=now)
        if wait > 0:
            self._record(user_id, key, source_ip, THROTTLED, now)
            raise TooManyAttemptsError(wait)

        secret = self._cipher.decrypt(secret_encrypted, aad=str(user_id).encode())
        step = verify_totp(secret, code, now=now.timestamp(), after_step=last_step)
        if step is None:
            self._record(user_id, key, source_ip, MFA_FAILED, now)
            raise AuthenticationError()
        self._record(user_id, key, source_ip, None, now)
        return step

    def _record(
        self,
        user_id: uuid.UUID,
        key: str,
        source_ip: str,
        failure: str | None,
        now: datetime,
    ) -> None:
        self._attempts.record(
            user_id=user_id,
            identifier_hash=key,
            source_ip=source_ip,
            device_summary=None,
            success=failure is None,
            failure_reason=failure,
            at=now,
        )
