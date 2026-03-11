from __future__ import annotations

import argparse
import json
from pathlib import Path

from plugins.provenance_guard.validator import validate_vector_write


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate vector write provenance payload")
    parser.add_argument("payload_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.payload_json).read_text(encoding="utf-8"))
    errors = validate_vector_write(payload)
    if errors:
        raise SystemExit("\n".join(errors))
    print("provenance validation passed")


if __name__ == "__main__":
    main()
