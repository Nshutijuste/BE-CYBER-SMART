"""Password hashing. Never write your own: use the vetted argon2-cffi library."""

import secrets
from functools import lru_cache

from argon2 import PasswordHasher as Argon2
from argon2 import Type
from argon2.exceptions import InvalidHashError, VerificationError

# OWASP minimum for Argon2id: 19 MiB memory, 2 passes, 1 lane.
MEMORY_COST_KIB = 19456
TIME_COST = 2
PARALLELISM = 1


def _make_argon2() -> Argon2:
    return Argon2(
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST_KIB,
        parallelism=PARALLELISM,
        type=Type.ID,
    )


@lru_cache(maxsize=1)
def _dummy_hash() -> str:
    """A real hash of a random value, made once. Used to waste the same time."""
    return _make_argon2().hash(secrets.token_urlsafe(16))


class Argon2PasswordHasher:
    def __init__(self) -> None:
        self._argon2 = _make_argon2()

    def hash(self, password: str) -> str:
        return self._argon2.hash(password)

    def verify(self, password_hash: str, password: str) -> bool:
        try:
            return self._argon2.verify(password_hash, password)
        except (VerificationError, InvalidHashError):
            return False

    def verify_dummy(self, password: str) -> None:
        """Take as long as a real check, so unknown accounts cannot be spotted by timing."""
        self.verify(_dummy_hash(), password)

    def needs_rehash(self, password_hash: str) -> bool:
        return self._argon2.check_needs_rehash(password_hash)