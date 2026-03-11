from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    paths = [
        "/home/netjer/.openclaw/memory/jabari.sqlite",
        "/home/netjer/.openclaw/memory/tariq.sqlite",
        "/home/netjer/.openclaw/memory/main.sqlite",
        "/home/netjer/.openclaw/memory/kimi.sqlite",
        "/home/netjer/.openclaw/memory/heru.sqlite",
        "/home/netjer/.openclaw/memory/haiku.sqlite",
        "/home/netjer/.openclaw/memory/arbiter.sqlite",
    ]
    print(json.dumps({"sqlite_audit": [{"path": p, "exists": Path(p).exists()} for p in paths]}, indent=2))


if __name__ == "__main__":
    main()
