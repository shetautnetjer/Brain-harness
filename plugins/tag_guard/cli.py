from __future__ import annotations

import argparse

from plugins.tag_guard.validator import validate_tags


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate tags against governed registry")
    parser.add_argument("--plane", default="plane_a", choices=["plane_a", "plane_b"])
    parser.add_argument("tags", nargs="+")
    args = parser.parse_args()

    result = validate_tags(args.tags, plane=args.plane)
    print(result)
    if result["errors"] and args.plane == "plane_b":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
