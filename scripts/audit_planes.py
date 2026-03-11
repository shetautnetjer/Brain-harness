from __future__ import annotations

import json


def main() -> None:
    report = {
        "mailbox_pattern": "/home/netjer/.openclaw/workspace/plane-a/mailbox/agents/<agent>/{inbox,outbox,received}",
        "checks": [
            "TODO: verify plane_a and plane_b table separation in live stores",
            "TODO: verify canonical_chunks_v2 write path enforces source_plane",
        ],
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
