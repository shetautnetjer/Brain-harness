# brain-harness

`brain-harness` is a governance + retrieval enforcement harness for an OpenClaw multi-agent memory runtime.

## What this repo does (and does not)
- Enforces doctrine in code at ingestion/retrieval boundaries.
- Preserves UUID provenance fields while keeping human-readable `doc_id`.
- Keeps Plane A and Plane B isolated in policy and validation.
- Implements deterministic-first retrieval routing (vectors are fallback only).
- Emits structured JSONL violations instead of silent drops.
- **Does not** pretend to provide fully-wired production DB adapters in this scaffold.

## Runtime inventory realism
Example manifests under `manifests/runtime/` are explicitly marked as `example` state.
Discovered runtime state should be produced via `scripts/collect_agent_state.py`, which reports known paths plus discovered existence checks.

Known path seeds include:
- `/home/netjer/.openclaw/workspace`
- `/home/netjer/.openclaw/workspace-jabari`
- `/home/netjer/.openclaw/workspace-tariq`
- `/home/netjer/.openclaw/workspace-kimi`
- `/home/netjer/.openclaw/workspace-heru`
- `/home/netjer/.openclaw/workspace-haiku`
- `/home/netjer/.openclaw/workspace-arbiter`
- `/home/netjer/.openclaw/memory/*.sqlite`
- `/home/netjer/.openclaw/workspace/plane-a/mailbox/agents/<agent>/{inbox,outbox,received}/`

## Setup
```bash
pip install -e .[dev]
pytest -q
```

## Validation entry points
```bash
python scripts/validate_qmd.py path/to/doc.qmd --plane plane_a
python scripts/validate_tags.py --plane plane_b memory doctrine
python scripts/validate_provenance.py payload.json
python scripts/collect_agent_state.py
```

## Current TODO boundaries
- Replace UUID fallback helper with true UUIDv7 implementation in runtime.
- Implement production-grade SQLite/LanceDB adapters.
- Add transaction-safe migration execution for `canonical_chunks_v2`.
