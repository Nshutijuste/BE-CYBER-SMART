import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MfaCredential(Base):
    """The authenticator secret is encrypted (AES-256-GCM), never stored as plain text."""

    __tablename__ = "mfa_credentials"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    secret_encrypted: Mapped[str] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(default=False, server_default="false")
    last_step: Mapped[int] = mapped_column(BigInteger, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
