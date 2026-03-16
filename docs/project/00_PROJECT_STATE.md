# 00 — Project State

## Verified in code
- Contracts, validators, retrieval router, and migration starter scripts are present.
- UUIDv7 event ID generation is implemented.
- Tag governance behavior is implemented (alias resolution, Plane A staging, Plane B rejection).
- Comms record schemas exist for envelope, delivery receipt, acknowledgement, notifier event, and shared comms identity.

## Verified in tests
- `tests/comms/test_comms_contracts.py` verifies authority-scope separation, UUIDv7 shape usage on concrete IDs, non-authoritative notifier behavior, and required comms tag bundle expectations.
- `tests/test_event_ids.py` verifies UUIDv7-based event ID format, uniqueness across calls, and prefix override behavior.

## Verified in runtime inventory
- Only **example** runtime manifests/snapshots are committed.
- Agent roots and mailbox path patterns are seeded, not runtime-proven.

## Settled doctrine
- Preserve Plane A vs Plane B separation.
- Kimi is sole Plane B writer as project doctrine (not presented as runtime-enforced in current committed code).
- Arbiter is final doctrine/tag/admission/promotion/violation authority.
- Files are authored truth; SQL is registry/join surface; vectors are indexes.

## Migration target
- Canonical chunk migration hardening.
- Envelope/event/mailbox contract grounding.
- Additive identity field alignment to UUIDv7 doctrine examples.
- Runtime evidence and enforcement for delivery/receipt/ack/replay/promotion semantics.

## Future idea / not yet implemented
- Guarantee-level delivery, receipt, acknowledgement, replay, and promotion behavior.
- Active Lobster runtime integration and broader llm-task expansion after grounding stabilizes.
