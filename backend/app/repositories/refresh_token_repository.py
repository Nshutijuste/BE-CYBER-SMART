import uuid
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models import RefreshToken
from app.domain.entities import RefreshTokenRecord
from app.repositories._time import aware


class SqlRefreshTokenRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        *,
        user_id: uuid.UUID,
        family_id: uuid.UUID,
        token_hash: str,
        mfa_passed: bool,
        created_at: datetime,
        expires_at: datetime,
    ) -> None:
        self._session.add(
            RefreshToken(
                user_id=user_id,
                family_id=family_id,
                token_hash=token_hash,
                mfa_passed=mfa_passed,
                created_at=created_at,
                expires_at=expires_at,
            )
        )
        self._session.commit()

    def get_by_hash(self, token_hash: str) -> RefreshTokenRecord | None:
        row = self._session.scalar(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        if row is None:
            return None
        return RefreshTokenRecord(
            id=row.id,
            user_id=row.user_id,
            family_id=row.family_id,
            mfa_passed=row.mfa_passed,
            expires_at=aware(row.expires_at),
            revoked_at=aware(row.revoked_at),
        )

    def revoke(self, token_id: uuid.UUID, at: datetime) -> None:
        self._session.execute(
            update(RefreshToken)
            .where(RefreshToken.id == token_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=at)
        )
        self._session.commit()

    def revoke_family(self, family_id: uuid.UUID, at: datetime) -> None:
        self._session.execute(
            update(RefreshToken)
            .where(RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=at)
        )
        self._session.commit()
