import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import ConflictError
from app.db.models import Role, User


class SqlUserRepository:
    """All user queries live here. No business rules."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def email_exists(self, email: str) -> bool:
        return self._session.scalar(select(User.id).where(User.email == email)) is not None

    def phone_exists(self, phone: str) -> bool:
        return self._session.scalar(select(User.id).where(User.phone == phone)) is not None

    def add(
        self,
        *,
        email: str | None,
        phone: str | None,
        password_hash: str,
        role: str,
    ) -> uuid.UUID:
        role_id = self._session.scalar(select(Role.id).where(Role.name == role))
        if role_id is None:
            raise RuntimeError(f"Role {role!r} is missing. Run the migrations.")

        user_id = uuid.uuid4()
        self._session.add(
            User(
                id=user_id,
                email=email,
                phone=phone,
                password_hash=password_hash,
                role_id=role_id,
            )
        )
        try:
            self._session.commit()
        except IntegrityError:
            # Two people registered the same details at the same moment.
            self._session.rollback()
            raise ConflictError() from None
        return user_id