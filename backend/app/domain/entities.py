import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredentials:
    """Just what login needs to know about a user."""

    id: uuid.UUID
    password_hash: str
    is_active: bool
