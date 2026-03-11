# 03 — Runtime Truth

## Verified in code
- `collect_agent_state.py` seeds `main` + peer agents and mailbox path conventions.
- Retrieval supports deterministic SQLite lookups and partial Plane B metadata lookup.

## Verified in runtime inventory
- Committed runtime files are examples (`manifest_state: example`, `snapshot_state: example`).
- No committed discovered inventory snapshot proving live mailbox/database health.

## Settled doctrine
- Aya identity = `main`.
- Shared operational workspace = `workspace` (`/home/netjer/.openclaw/workspace`).

## Migration target
- Promote discovered runtime snapshots into committed verified inventory artifacts.

## Future idea / not yet implemented
- Guaranteed mailbox delivery/receipts/replay semantics.
