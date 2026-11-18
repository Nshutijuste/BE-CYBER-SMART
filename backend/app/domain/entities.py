import uuid
from dataclasses import dataclass
from datetime import datetime

# Failures that count toward a lockout. "throttled" attempts never count,
# so an attacker cannot make a real user's lockout last forever.
COUNTED_FAILURES = frozenset({"wrong_password", "unknown_account", "mfa_failed"})


@dataclass(frozen=True)
class UserCredentials:
    """Just what login needs to know about a user."""

    id: uuid.UUID
    password_hash: str
    is_active: bool


@dataclass(frozen=True)
class UserProfile:
    id: uuid.UUID
    role: str
    is_active: bool


@dataclass(frozen=True)
class RefreshTokenRecord:
    id: uuid.UUID
    user_id: uuid.UUID
    family_id: uuid.UUID
    mfa_passed: bool
    expires_at: datetime
    revoked_at: datetime | None


@dataclass(frozen=True)
class MfaState:
    secret_encrypted: str
    enabled: bool
    last_step: int


@dataclass(frozen=True)
class FailureWindow:
    count: int
    last_at: datetime | None
