from __future__ import annotations

REQUIRED_VECTOR_FIELDS = [
    "embedding_model",
    "embedding_dim",
    "source_plane",
    "ingest_run_id",
    "indexed_at",
]


def validate_vector_write(payload: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_VECTOR_FIELDS:
        if field not in payload:
            errors.append(f"missing required provenance field: {field}")
    return errors


def validate_plane_separation(existing_plane: str | None, incoming_plane: str) -> list[str]:
    if existing_plane and existing_plane != incoming_plane:
        return [f"plane separation violation: existing={existing_plane}, incoming={incoming_plane}"]
    return []
