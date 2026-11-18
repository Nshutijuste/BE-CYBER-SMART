"""Keyed hashing and field encryption. Vetted library only: cryptography."""

import base64
import hashlib
import hmac
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def derive_key(secret: str, purpose: str) -> bytes:
    """One secret in .env, a separate 32-byte key for each purpose."""
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=f"bcs:{purpose}".encode(),
    ).derive(secret.encode())


class KeyedHasher:
    """HMAC-SHA-256 with a secret key. Same input, same output, but not reversible
    without the key (a plain hash of a phone number is easy to reverse)."""

    def __init__(self, secret: str) -> None:
        self._key = derive_key(secret, "hmac-v1")

    def __call__(self, value: str) -> str:
        return hmac.new(self._key, value.encode(), hashlib.sha256).hexdigest()


class FieldCipher:
    """AES-256-GCM: a new random nonce each time, a version label for key rotation,
    and optional 'associated data' that ties the ciphertext to one owner."""

    VERSION = "v1"

    def __init__(self, secret: str) -> None:
        self._aes = AESGCM(derive_key(secret, "field-aes-v1"))

    def encrypt(self, plaintext: str, *, aad: bytes = b"") -> str:
        nonce = os.urandom(12)
        sealed = self._aes.encrypt(nonce, plaintext.encode(), aad)
        return f"{self.VERSION}.{base64.urlsafe_b64encode(nonce + sealed).decode()}"

    def decrypt(self, token: str, *, aad: bytes = b"") -> str:
        version, _, body = token.partition(".")
        if version != self.VERSION:
            raise ValueError("unknown key version")
        raw = base64.urlsafe_b64decode(body.encode())
        return self._aes.decrypt(raw[:12], raw[12:], aad).decode()
