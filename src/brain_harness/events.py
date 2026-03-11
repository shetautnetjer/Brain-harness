from __future__ import annotations

import secrets
import time
from datetime import UTC, datetime
from uuid import UUID


def _uuid7() -> UUID:
    """Generate a RFC 9562 UUIDv7 using unix epoch milliseconds and randomness."""
    timestamp_ms = int(time.time_ns() // 1_000_000) & ((1 << 48) - 1)
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)

    value = 0
    value |= timestamp_ms << 80
    value |= 0x7 << 76  # version 7
    value |= rand_a << 64
    value |= 0b10 << 62  # RFC 4122/9562 variant
    value |= rand_b
    return UUID(int=value)


def make_event_id(prefix: str = "evt") -> str:
    return f"{prefix}_{_uuid7()}"


def iso_utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
