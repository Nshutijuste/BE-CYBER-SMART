from datetime import UTC, datetime


def aware(value: datetime | None) -> datetime | None:
    """Some databases hand back times without a zone. Ours are always UTC."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value
