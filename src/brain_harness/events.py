from __future__ import annotations

from datetime import datetime
from uuid import uuid4


def make_event_id(prefix: str = "evt") -> str:
    """TODO: replace uuid4 fallback with true UUIDv7 library in runtime."""
    return f"{prefix}_{uuid4()}"


def iso_utc_now() -> str:
    return datetime.utcnow().isoformat() + "Z"
