from __future__ import annotations

import json
from pathlib import Path

KNOWN = {
    "jabari": "/home/netjer/.openclaw/workspace-jabari",
    "tariq": "/home/netjer/.openclaw/workspace-tariq",
    "kimi": "/home/netjer/.openclaw/workspace-kimi",
    "heru": "/home/netjer/.openclaw/workspace-heru",
    "haiku": "/home/netjer/.openclaw/workspace-haiku",
    "main": "/home/netjer/.openclaw/workspace",
    "arbiter": "/home/netjer/.openclaw/workspace-arbiter",
}


def collect() -> dict:
    rows = []
    for agent, path in KNOWN.items():
        p = Path(path)
        rows.append({"agent": agent, "root_dir": path, "exists": p.exists()})
    return {"agents": rows}


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
