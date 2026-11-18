"""Has this password appeared in a known data leak? Uses the free Pwned Passwords
range service. Only the first 5 characters of a SHA-1 are sent, never the password."""

import hashlib
import logging

import httpx

logger = logging.getLogger(__name__)

RANGE_URL = "https://api.pwnedpasswords.com/range/"


class PwnedPasswordsChecker:
    def __init__(self, client: httpx.Client | None = None, timeout: float = 2.0) -> None:
        self._client = client
        self._timeout = timeout

    def is_breached(self, password: str) -> bool:
        # SHA-1 is required by this service's protocol. It is not how we store passwords.
        digest = hashlib.sha1(password.encode(), usedforsecurity=False).hexdigest().upper()
        prefix, suffix = digest[:5], digest[5:]
        headers = {"Add-Padding": "true", "User-Agent": "BeCyberSmart-password-check"}
        try:
            if self._client is not None:
                response = self._client.get(RANGE_URL + prefix, headers=headers)
            else:
                with httpx.Client(timeout=self._timeout) as client:
                    response = client.get(RANGE_URL + prefix, headers=headers)
            response.raise_for_status()
        except httpx.HTTPError:
            # If the service is down we let people register, and we say so in the log.
            logger.warning("breach_check_unavailable")
            return False
        for line in response.text.splitlines():
            found, _, count = line.partition(":")
            if found.strip().upper() == suffix and int(count.strip() or 0) > 0:
                return True  # count 0 lines are padding
        return False
