from __future__ import annotations

from dataclasses import dataclass

import yaml


@dataclass
class QmdDocument:
    frontmatter: dict
    body: str


def parse_qmd(content: str) -> QmdDocument:
    if not content.startswith("---\n"):
        raise ValueError("QMD file missing YAML frontmatter start")
    parts = content.split("\n---\n", maxsplit=1)
    if len(parts) != 2:
        raise ValueError("QMD file missing YAML frontmatter terminator")
    raw_frontmatter = parts[0].replace("---\n", "", 1)
    frontmatter = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("QMD frontmatter must parse as mapping")
    return QmdDocument(frontmatter=frontmatter, body=parts[1])
