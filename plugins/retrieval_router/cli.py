from __future__ import annotations

import argparse

from plugins.retrieval_router.router import route_query


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic-first retrieval router")
    parser.add_argument("query")
    args = parser.parse_args()
    print(route_query(args.query).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
