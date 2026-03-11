from __future__ import annotations

import argparse

from src.brain_harness.jsonl import emit_jsonl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="artifacts/violations.jsonl")
    parser.add_argument("--event-type", required=True)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()
    emit_jsonl(args.path, {"event_type": args.event_type, "message": args.message})


if __name__ == "__main__":
    main()
