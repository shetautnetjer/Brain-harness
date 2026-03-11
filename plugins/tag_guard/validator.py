from __future__ import annotations

from pathlib import Path

import yaml

from src.brain_harness.events import iso_utc_now
from src.brain_harness.jsonl import emit_jsonl


def load_registry(path: str = "registries/tag_registry.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _maps(registry: dict) -> tuple[set[str], dict[str, str]]:
    canonical = set()
    aliases: dict[str, str] = {}
    for row in registry.get("tags", []):
        c = row["canonical_tag"]
        canonical.add(c)
        for alias in row.get("aliases", []):
            aliases[alias] = c
    return canonical, aliases


def validate_tags(tags: list[str], plane: str, pending_path: str = "registries/pending_tags.jsonl") -> dict:
    registry = load_registry()
    canonical, aliases = _maps(registry)

    errors: list[str] = []
    resolved: list[str] = []

    for raw in tags:
        tag = raw.strip().lower()
        final = aliases.get(tag, tag)
        if final in canonical:
            resolved.append(final)
            continue

        payload = {"tag": tag, "plane": plane, "timestamp": iso_utc_now(), "status": "pending"}
        if plane == "plane_a":
            emit_jsonl(pending_path, payload)
            errors.append(f"unknown tag staged for review: {tag}")
        else:
            errors.append(f"unknown tag rejected on plane_b: {tag}")

    return {"resolved_tags": sorted(set(resolved)), "errors": errors}
