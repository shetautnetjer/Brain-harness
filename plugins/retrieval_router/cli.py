from __future__ import annotations

import argparse

from plugins.retrieval_router.router import route_query


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic-first retrieval router")
    parser.add_argument("query")
    parser.add_argument("--agent", default="main")
    parser.add_argument("--local-db-path")
    parser.add_argument("--plane-b-db-path")
    parser.add_argument("--force-plane-b", action="store_true")
    args = parser.parse_args()
    print(
        route_query(
            args.query,
            force_plane_b=args.force_plane_b,
            agent=args.agent,
            local_db_path=args.local_db_path,
            plane_b_db_path=args.plane_b_db_path,
        ).model_dump_json(indent=2)
    )


if __name__ == "__main__":
    main()
