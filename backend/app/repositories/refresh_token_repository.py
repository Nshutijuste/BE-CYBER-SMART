import uuid
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models import RefreshToken
from app.domain.entities import RefreshTokenRecord, RefreshTokenRotationResult
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
        return self._record(row) if row is not None else None

    def rotate(
        self,
        *,
        token_hash: str,
        replacement_hash: str,
        at: datetime,
        replacement_expires_at: datetime,
    ) -> RefreshTokenRotationResult:
        row = self._session.scalar(
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        if row is None:
            return RefreshTokenRotationResult(record=None, replayed=False)

        record = self._record(row)
        if row.revoked_at is not None:
            self._session.execute(
                update(RefreshToken)
                .where(
                    RefreshToken.family_id == row.family_id,
                    RefreshToken.revoked_at.is_(None),
                )
                .values(revoked_at=at)
            )
            self._session.commit()
            return RefreshTokenRotationResult(record=record, replayed=True)

        expiry = aware(row.expires_at)
        if expiry is None or expiry <= at:
            return RefreshTokenRotationResult(record=None, replayed=False)

        row.revoked_at = at
        self._session.add(
            RefreshToken(
                user_id=row.user_id,
                family_id=row.family_id,
                token_hash=replacement_hash,
                mfa_passed=row.mfa_passed,
                created_at=at,
                expires_at=replacement_expires_at,
            )
        )
        self._session.commit()
        return RefreshTokenRotationResult(record=record, replayed=False)

    def revoke_family(self, family_id: uuid.UUID, at: datetime) -> None:
        self._session.execute(
            update(RefreshToken)
            .where(RefreshToken.family_id == family_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=at)
        )
        self._session.commit()

    @staticmethod
    def _record(row: RefreshToken) -> RefreshTokenRecord:
        return RefreshTokenRecord(
            id=row.id,
            user_id=row.user_id,
            family_id=row.family_id,
            mfa_passed=row.mfa_passed,
            expires_at=aware(row.expires_at),
            revoked_at=aware(row.revoked_at),
        )
