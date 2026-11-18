import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class LoggingNotifier:
    """For now a notice is a log line. A real email provider replaces this class later."""

    def new_device_login(
        self,
        *,
        user_id: uuid.UUID,
        device_summary: str | None,
        source_ip: str,
        at: datetime,
    ) -> None:
        logger.info(
            "new_device_login user=%s ip=%s device=%s at=%s",
            user_id,
            source_ip,
            (device_summary or "unknown")[:80],
            at.isoformat(),
        )
