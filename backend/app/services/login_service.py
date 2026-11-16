import uuid

from app.core.errors import AuthenticationError
from app.domain.interfaces import LoginAttemptRepository, PasswordHasher, UserRepository
from app.schemas.auth import LoginRequest

UNKNOWN_ACCOUNT = "unknown_account"
WRONG_PASSWORD = "wrong_password"
INACTIVE_ACCOUNT = "inactive_account"


class LoginService:
    def __init__(
        self,
        users: UserRepository,
        attempts: LoginAttemptRepository,
        hasher: PasswordHasher,
    ) -> None:
        self._users = users
        self._attempts = attempts
        self._hasher = hasher

    def login(
        self,
        data: LoginRequest,
        *,
        source_ip: str,
        device_summary: str | None,
    ) -> uuid.UUID:
        email = data.email.lower() if data.email else None
        password = data.password.get_secret_value()
        found = self._users.find_for_login(email=email, phone=data.phone)

        user_id: uuid.UUID | None = None
        failure: str | None = None
        if found is None:
            self._hasher.verify_dummy(password)
            failure = UNKNOWN_ACCOUNT
        else:
            user_id = found.id
            if not self._hasher.verify(found.password_hash, password):
                failure = WRONG_PASSWORD
            elif not found.is_active:
                failure = INACTIVE_ACCOUNT

        self._attempts.record(
            user_id=user_id,
            source_ip=source_ip,
            device_summary=device_summary,
            success=failure is None,
            failure_reason=failure,
        )
        if failure is not None or user_id is None:
            raise AuthenticationError()
        return user_id
