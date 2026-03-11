from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from uuid6 import uuid7


def _uuid7() -> UUID:
    """Generate a RFC 9562 UUIDv7."""
    return uuid7()


def make_event_id(prefix: str = "evt") -> str:
    return f"{prefix}_{_uuid7()}"


def iso_utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
