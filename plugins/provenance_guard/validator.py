from __future__ import annotations

from datetime import datetime
from typing import Any

REQUIRED_VECTOR_FIELDS = [
    "embedding_model",
    "embedding_dim",
    "source_plane",
    "ingest_run_id",
    "indexed_at",
]


def _is_iso8601(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_vector_write(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_VECTOR_FIELDS:
        if field not in payload:
            errors.append(f"missing required provenance field: {field}")

    if "embedding_dim" in payload and (not isinstance(payload["embedding_dim"], int) or payload["embedding_dim"] <= 0):
        errors.append("embedding_dim must be a positive integer")

    if payload.get("source_plane") not in {"plane_a", "plane_b"}:
        errors.append("source_plane must be one of: plane_a, plane_b")

    if "indexed_at" in payload and not _is_iso8601(str(payload["indexed_at"])):
        errors.append("indexed_at must be an ISO-8601 timestamp")

    return errors


def validate_plane_separation(existing_plane: str | None, incoming_plane: str) -> list[str]:
    if existing_plane and existing_plane != incoming_plane:
        return [f"plane separation violation: existing={existing_plane}, incoming={incoming_plane}"]
    return []


def validate_batch_plane_consistency(rows: list[dict[str, Any]]) -> list[str]:
    planes = {row.get("source_plane") for row in rows if row.get("source_plane")}
    if len(planes) > 1:
        return [f"plane separation violation: mixed source_plane values in batch: {sorted(planes)}"]
    return []
