import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import ConflictError
from app.db.models import Role, User
from app.domain.entities import UserCredentials, UserProfile


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

    def find_for_login(
        self, *, email: str | None, phone: str | None
    ) -> UserCredentials | None:
        query = select(User.id, User.password_hash, User.is_active)
        if email is not None:
            query = query.where(User.email == email)
        elif phone is not None:
            query = query.where(User.phone == phone)
        else:
            return None
        row = self._session.execute(query).first()
        if row is None:
            return None
        return UserCredentials(
            id=row.id, password_hash=row.password_hash, is_active=row.is_active
        )

    def find_by_id(self, user_id: uuid.UUID) -> UserProfile | None:
        row = self._session.execute(
            select(User.id, Role.name, User.is_active)
            .join(Role, Role.id == User.role_id)
            .where(User.id == user_id)
        ).first()
        if row is None:
            return None
        return UserProfile(id=row.id, role=row.name, is_active=row.is_active)
