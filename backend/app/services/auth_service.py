import uuid

from app.core.errors import ConflictError, WeakPasswordError
from app.domain.interfaces import BreachChecker, PasswordHasher, UserRepository
from app.schemas.auth import RegisterRequest

SUBSCRIBER_ROLE = "subscriber"


class AuthService:
    def __init__(
        self,
        users: UserRepository,
        hasher: PasswordHasher,
        breach_checker: BreachChecker,
    ) -> None:
        self._users = users
        self._hasher = hasher
        self._breach = breach_checker

    def register(self, data: RegisterRequest) -> uuid.UUID:
        password = data.password.get_secret_value()
        if self._breach.is_breached(password):
            raise WeakPasswordError()

        # Hash first, so a taken address and a free one take about the same time.
        password_hash = self._hasher.hash(password)
        email = data.email.lower() if data.email else None

        taken = (email is not None and self._users.email_exists(email)) or (
            data.phone is not None and self._users.phone_exists(data.phone)
        )
        if taken:
            raise ConflictError()

        return self._users.add(
            email=email,
            phone=data.phone,
            password_hash=password_hash,
            role=SUBSCRIBER_ROLE,
        )
