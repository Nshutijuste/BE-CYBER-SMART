"""Signed tokens (JWT, EdDSA). Short-lived. Only our server can make or check them."""

import secrets
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.core.crypto import derive_key

ISSUER = "be-cyber-smart"
AUDIENCE = "be-cyber-smart-web"
ACCESS = "access"
MFA_CHALLENGE = "mfa"


class InvalidTokenError(Exception):
    """The token is missing, forged, expired or of the wrong kind."""


@dataclass(frozen=True)
class AccessClaims:
    user_id: uuid.UUID
    mfa: bool


class TokenService:
    def __init__(
        self,
        secret: str,
        *,
        access_lifetime: timedelta = timedelta(minutes=15),
        challenge_lifetime: timedelta = timedelta(minutes=5),
    ) -> None:
        self._private = Ed25519PrivateKey.from_private_bytes(derive_key(secret, "jwt-ed25519-v1"))
        self._public = self._private.public_key()
        self._access_lifetime = access_lifetime
        self._challenge_lifetime = challenge_lifetime

    def _encode(self, user_id: uuid.UUID, kind: str, lifetime: timedelta, **extra) -> str:
        now = datetime.now(UTC)
        payload = {
            "iss": ISSUER,
            "aud": AUDIENCE,
            "sub": str(user_id),
            "typ": kind,
            "iat": now,
            "exp": now + lifetime,
            "jti": secrets.token_urlsafe(12),
            **extra,
        }
        return jwt.encode(payload, self._private, algorithm="EdDSA")

    def _decode(self, token: str, kind: str) -> dict:
        try:
            claims = jwt.decode(
                token,
                self._public,
                algorithms=["EdDSA"],  # never "none", never anything else
                audience=AUDIENCE,
                issuer=ISSUER,
                options={"require": ["exp", "iat", "sub", "jti", "typ"]},
            )
            if claims["typ"] != kind:
                raise InvalidTokenError
            uuid.UUID(claims["sub"])
        except (jwt.PyJWTError, ValueError, TypeError) as exc:
            raise InvalidTokenError from exc
        return claims

    def issue_access(self, user_id: uuid.UUID, *, mfa: bool) -> str:
        return self._encode(user_id, ACCESS, self._access_lifetime, mfa=mfa)

    def decode_access(self, token: str) -> AccessClaims:
        claims = self._decode(token, ACCESS)
        return AccessClaims(user_id=uuid.UUID(claims["sub"]), mfa=bool(claims.get("mfa", False)))

    def issue_mfa_challenge(self, user_id: uuid.UUID) -> str:
        return self._encode(user_id, MFA_CHALLENGE, self._challenge_lifetime)

    def decode_mfa_challenge(self, token: str) -> uuid.UUID:
        return uuid.UUID(self._decode(token, MFA_CHALLENGE)["sub"])
