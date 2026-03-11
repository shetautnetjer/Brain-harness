from __future__ import annotations

from pathlib import Path
import yaml


def main() -> None:
    registry = yaml.safe_load(Path("registries/tag_registry.yaml").read_text(encoding="utf-8"))
    tags = [t["canonical_tag"] for t in registry.get("tags", [])]
    print("canonical tags:")
    for t in tags:
        print(f"- {t}")


if __name__ == "__main__":
    main()
