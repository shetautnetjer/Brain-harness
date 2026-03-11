from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from plugins.tag_guard.normalize import normalize_doc_id
from plugins.tag_guard.validator import validate_tags


def load_doc_type_rules(path: str = "registries/doc_type_rules.yaml") -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def validate_frontmatter(frontmatter: dict[str, Any], plane: str, doc_type_rules: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ["doc_id", "doc_type", "tags"]
    for field in required:
        if field not in frontmatter:
            errors.append(f"missing required field: {field}")

    if "doc_id" in frontmatter:
        frontmatter["doc_id"] = normalize_doc_id(str(frontmatter["doc_id"]))

    if "tags" in frontmatter and not isinstance(frontmatter["tags"], list):
        errors.append("tags must be a list in frontmatter")
        return errors

    tags = frontmatter.get("tags", [])
    tag_result = validate_tags(tags=tags, plane=plane)
    errors.extend(tag_result["errors"])
    frontmatter["tags"] = tag_result["resolved_tags"]

    rules = doc_type_rules.get("doc_type_rules", {})
    doc_type = frontmatter.get("doc_type")
    rule = rules.get(doc_type, {})

    # Plane B requires source_events by default; only explicit exemptions turn this off.
    source_events_required = bool(rule.get("require_source_events_on_plane_b", True))

    if plane == "plane_b" and source_events_required and not frontmatter.get("source_events"):
        errors.append("source_events required for this doc_type on plane_b")

    return errors
