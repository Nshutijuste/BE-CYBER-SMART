"""Password hashing. Never write your own: use the vetted argon2-cffi library."""

from argon2 import PasswordHasher as Argon2
from argon2 import Type
from argon2.exceptions import InvalidHashError, VerificationError

# OWASP minimum for Argon2id: 19 MiB memory, 2 passes, 1 lane.
MEMORY_COST_KIB = 19456
TIME_COST = 2
PARALLELISM = 1


class Argon2PasswordHasher:
    def __init__(self) -> None:
        self._argon2 = Argon2(
            time_cost=TIME_COST,
            memory_cost=MEMORY_COST_KIB,
            parallelism=PARALLELISM,
            type=Type.ID,
        )

    def hash(self, password: str) -> str:
        return self._argon2.hash(password)

    def verify(self, password_hash: str, password: str) -> bool:
        try:
            return self._argon2.verify(password_hash, password)
        except (VerificationError, InvalidHashError):
            return False

    def needs_rehash(self, password_hash: str) -> bool:
        return self._argon2.check_needs_rehash(password_hash)