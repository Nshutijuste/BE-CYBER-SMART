import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    __table_args__ = (
        Index("ix_login_attempts_user_time", "user_id", "attempted_at"),
        Index("ix_login_attempts_ip_time", "source_ip", "attempted_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    source_ip: Mapped[str] = mapped_column(String(45))
    device_summary: Mapped[str | None] = mapped_column(String(200))
    success: Mapped[bool]
    failure_reason: Mapped[str | None] = mapped_column(String(50))