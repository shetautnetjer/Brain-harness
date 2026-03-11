from __future__ import annotations

import argparse
from pathlib import Path

from plugins.qmd_guard.parser import parse_qmd
from plugins.qmd_guard.validator import load_doc_type_rules, validate_frontmatter


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate QMD frontmatter")
    parser.add_argument("qmd_path")
    parser.add_argument("--plane", default="plane_a", choices=["plane_a", "plane_b"])
    args = parser.parse_args()

    content = Path(args.qmd_path).read_text(encoding="utf-8")
    doc = parse_qmd(content)
    errors = validate_frontmatter(doc.frontmatter, plane=args.plane, doc_type_rules=load_doc_type_rules())
    if errors:
        raise SystemExit("\n".join(errors))
    print("QMD validation passed")


if __name__ == "__main__":
    main()
