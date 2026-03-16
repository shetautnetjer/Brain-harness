# 03 — Runtime Truth

## Verified in code
- `scripts/collect_agent_state.py` seeds known agent roots (`main`, `jabari`, `tariq`, `kimi`, `heru`, `haiku`, `arbiter`) and mailbox path conventions.
- Retrieval supports deterministic SQLite lookups and partial Plane B metadata lookup.

## Verified in tests
- Automated tests cover comms schema/example shape and retrieval/event-id behavior.
- Current tests do **not** prove live runtime mailbox health, guaranteed delivery, guaranteed receipt, guaranteed acknowledgement, guaranteed replay, or guaranteed promotion.

## Verified in runtime inventory
- Committed runtime files are examples (`manifest_state: example`, `snapshot_state: example`).
- No committed discovered inventory snapshot proves live mailbox/database health.

## Settled doctrine
- Aya identity = `main`.
- Shared operational workspace = `workspace` (`/home/netjer/.openclaw/workspace`).
- Preserve Plane A vs Plane B separation.

## Migration target
- Promote discovered runtime snapshots into committed verified inventory artifacts.
- Add runtime evidence for mailbox/ledger health before making stronger runtime claims.

## Future idea / not yet implemented
- Runtime-level guarantee semantics for delivery, receipt, acknowledgement, replay, and promotion.
- Active Lobster runtime integration for comms operations.
