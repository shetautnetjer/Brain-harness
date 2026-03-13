from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.brain_harness.events import iso_utc_now
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
        tag = str(raw).strip().lower()
        if not tag:
            continue

        final = aliases.get(tag, tag)
        allowed_planes = canonical.get(final)
        if allowed_planes and plane in allowed_planes:
            resolved.append(final)
            continue

        payload = {"tag": tag, "plane": plane, "timestamp": iso_utc_now(), "status": "pending"}
        if plane == "plane_a":
            emit_jsonl(pending_path, payload)
            msg = f"unknown tag staged for review: {tag}"
            errors.append(msg)
            _emit_taxonomy_violation(
                violation_path,
                "warning",
                msg,
                {"tag": tag, "plane": plane, "action": "staged_pending"},
            )
        else:
            msg = f"unknown tag rejected on plane_b: {tag}"
            errors.append(msg)
            _emit_taxonomy_violation(
                violation_path,
                "error",
                msg,
                {"tag": tag, "plane": plane, "action": "rejected"},
            )

    return {"resolved_tags": sorted(set(resolved)), "errors": errors}
