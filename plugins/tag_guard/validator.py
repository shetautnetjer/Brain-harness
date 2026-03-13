from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.brain_harness.events import iso_utc_now, make_event_id
from src.brain_harness.jsonl import emit_jsonl


def load_registry(path: str = "registries/tag_registry.yaml") -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _maps(registry: dict[str, Any]) -> tuple[dict[str, set[str]], dict[str, str]]:
    canonical: dict[str, set[str]] = {}
    aliases: dict[str, str] = {}
    for row in registry.get("tags", []):
        c = str(row["canonical_tag"]).strip().lower()
        canonical[c] = {str(p).strip().lower() for p in row.get("planes_allowed", [])}
        for alias in row.get("aliases", []):
            aliases[str(alias).strip().lower()] = c
    return canonical, aliases


def _emit_taxonomy_violation(path: str, severity: str, message: str, context: dict[str, Any]) -> None:
    emit_jsonl(
        path,
        {
            "event_type": "taxonomy_violation",
            "severity": severity,
            "message": message,
            "context": context,
            "timestamp": iso_utc_now(),
        },
    )


def validate_tags(
    tags: list[str],
    plane: str,
    pending_path: str = "registries/pending_tags.jsonl",
    violation_path: str = "audits/violations.jsonl",
) -> dict[str, Any]:
    registry = load_registry()
    canonical, aliases = _maps(registry)

    errors: list[str] = []
    resolved: list[str] = []

    for raw in tags:
        normalized_tag = str(raw).strip().lower()
        if not normalized_tag:
            continue

        resolved_tag = aliases.get(normalized_tag, normalized_tag)
        allowed_planes = canonical.get(resolved_tag)
        resolution_status = "resolved_canonical" if allowed_planes else "unresolved"

        if resolution_status == "resolved_canonical" and plane in allowed_planes:
            resolved.append(resolved_tag)
            continue

        timestamp = iso_utc_now()
        common_context = {
            "raw_tag": raw,
            "normalized_tag": normalized_tag,
            "resolved_tag": resolved_tag if resolution_status == "resolved_canonical" else None,
            "resolution_status": resolution_status,
            "plane": plane,
            "timestamp": timestamp,
            "event_id": make_event_id("tag_guard"),
        }

        if resolution_status == "unresolved" and plane == "plane_a":
            payload = {
                "tag": normalized_tag,
                "plane": plane,
                "timestamp": timestamp,
                "status": "pending",
                "action": "staged_pending_unknown",
                "reason": "unknown_unresolved_tag",
                **common_context,
            }
            emit_jsonl(pending_path, payload)
            msg = f"unknown tag staged for review: {normalized_tag}"
            errors.append(msg)
            _emit_taxonomy_violation(
                violation_path,
                "warning",
                msg,
                {
                    **common_context,
                    "action": "staged_pending_unknown",
                    "reason": "unknown_unresolved_tag",
                },
            )
            continue

        if resolution_status == "unresolved":
            msg = f"unknown tag rejected on plane_b: {normalized_tag}"
            errors.append(msg)
            _emit_taxonomy_violation(
                violation_path,
                "error",
                msg,
                {
                    **common_context,
                    "action": "rejected_unknown_plane_b",
                    "reason": "unknown_unresolved_tag",
                },
            )
            continue

        msg = f"tag not allowed on {plane}: {resolved_tag}"
        errors.append(msg)
        _emit_taxonomy_violation(
            violation_path,
            "error",
            msg,
            {
                **common_context,
                "action": "rejected_plane_disallowed",
                "reason": "plane_disallowed",
            },
        )

    return {"resolved_tags": sorted(set(resolved)), "errors": errors}
