"""Time-based one-time codes (RFC 6238), the kind authenticator apps show."""

import hmac
import time

import pyotp

STEP_SECONDS = 30
ISSUER_NAME = "Be Cyber Smart"


def new_secret() -> str:
    return pyotp.random_base32()


def provisioning_uri(secret: str, account: str) -> str:
    return pyotp.TOTP(secret).provisioning_uri(name=account, issuer_name=ISSUER_NAME)


def verify_totp(
    secret: str,
    code: str,
    *,
    now: float | None = None,
    after_step: int = 0,
) -> int | None:
    """Return the matching time step, or None. A step at or before `after_step` was
    already used, so a code can never be used twice."""
    code = code.strip()
    if not (code.isascii() and code.isdigit() and len(code) == 6):
        return None
    current = int((time.time() if now is None else now) // STEP_SECONDS)
    totp = pyotp.TOTP(secret)
    for step in (current - 1, current, current + 1):  # one step of clock drift each way
        if step > after_step and hmac.compare_digest(totp.generate_otp(step), code):
            return step
    return None
