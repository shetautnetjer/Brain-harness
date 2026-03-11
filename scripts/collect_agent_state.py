from __future__ import annotations

import json
from pathlib import Path

KNOWN_ROOTS = {
    "main": "/home/netjer/.openclaw/workspace",
    "jabari": "/home/netjer/.openclaw/workspace-jabari",
    "tariq": "/home/netjer/.openclaw/workspace-tariq",
    "kimi": "/home/netjer/.openclaw/workspace-kimi",
    "heru": "/home/netjer/.openclaw/workspace-heru",
    "haiku": "/home/netjer/.openclaw/workspace-haiku",
    "arbiter": "/home/netjer/.openclaw/workspace-arbiter",
}

MAILBOX_BASE = "/home/netjer/.openclaw/workspace/plane-a/mailbox/agents"
SQLITE_GLOB = "/home/netjer/.openclaw/memory/*.sqlite"


def collect() -> dict:
    rows = []
    for agent, path in KNOWN_ROOTS.items():
        p = Path(path)
        rows.append(
            {
                "agent": agent,
                "known_example_root_dir": path,
                "discovered_exists": p.exists(),
            }
        )

    sqlite_paths = [str(p) for p in sorted(Path("/home/netjer/.openclaw/memory").glob("*.sqlite"))]

    mailbox_dirs = {}
    for agent in KNOWN_ROOTS:
        mailbox_dirs[agent] = {
            "inbox": f"{MAILBOX_BASE}/{agent}/inbox",
            "outbox": f"{MAILBOX_BASE}/{agent}/outbox",
            "received": f"{MAILBOX_BASE}/{agent}/received",
        }

    return {
        "snapshot_kind": "runtime_inventory",
        "known_example_state": True,
        "known_sqlite_glob": SQLITE_GLOB,
        "agents": rows,
        "discovered_sqlite_paths": sqlite_paths,
        "mailbox_dirs": mailbox_dirs,
    }


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
