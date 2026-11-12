import uuid

from app.core.errors import ConflictError
from app.domain.interfaces import PasswordHasher, UserRepository
from app.schemas.auth import RegisterRequest

SUBSCRIBER_ROLE = "subscriber"


class AuthService:
    def __init__(self, users: UserRepository, hasher: PasswordHasher) -> None:
        self._users = users
        self._hasher = hasher

    def register(self, data: RegisterRequest) -> uuid.UUID:
        # Hash first, so a taken address and a free one take about the same time.
        password_hash = self._hasher.hash(data.password.get_secret_value())
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