"""Progressive lockout. Five free failures, then a growing wait. Never permanent."""

import logging
import math
from datetime import datetime, timedelta

from app.domain.interfaces import LoginAttemptRepository

logger = logging.getLogger(__name__)

WINDOW = timedelta(minutes=15)
FREE_FAILURES = 5
BASE_DELAY_SECONDS = 30
MAX_DELAY_SECONDS = 900
IP_FAILURE_LIMIT = 20  # many failures from one address across many accounts: spraying
IP_RETRY_SECONDS = 60


def lock_seconds(failures: int) -> int:
    """0 for the first five failures, then 30, 60, 120 ... up to 900 seconds."""
    if failures < FREE_FAILURES:
        return 0
    exponent = min(failures - FREE_FAILURES, 10)
    return min(BASE_DELAY_SECONDS * 2**exponent, MAX_DELAY_SECONDS)


def seconds_left(failures: int, last_failure: datetime | None, now: datetime) -> int:
    if last_failure is None:
        return 0
    left = lock_seconds(failures) - (now - last_failure).total_seconds()
    return max(0, math.ceil(left))


class Throttle:
    def __init__(self, attempts: LoginAttemptRepository) -> None:
        self._attempts = attempts

    def wait_seconds(self, *, key_hash: str, source_ip: str, now: datetime) -> int:
        """How long this caller must wait. 0 means go ahead."""
        since = now - WINDOW
        if self._attempts.failures_from_ip(source_ip, since) >= IP_FAILURE_LIMIT:
            logger.warning("password_spraying_suspected ip=%s", source_ip)
            return IP_RETRY_SECONDS
        window = self._attempts.failure_window(key_hash, since)
        return seconds_left(window.count, window.last_at, now)
