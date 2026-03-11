# 00 — Project State

## Verified in code
- Contracts, validators, retrieval router, and migration starter scripts are present and tested.
- UUIDv7 event ID generation exists and is tested.
- Tag governance behavior is implemented (alias resolution, Plane A staging, Plane B rejection).

## Verified in runtime inventory
- Only **example** runtime manifests/snapshots are committed.
- Agent roots and mailbox path patterns are seeded, not runtime-proven.

## Settled doctrine
- Preserve Plane A vs Plane B separation.
- Kimi is sole Plane B writer.
- Arbiter is final doctrine/tag/admission/promotion/violation authority.
- Files are authored truth; SQL is registry/join surface; vectors are indexes.

## Migration target
- Canonical chunk migration hardening.
- Envelope/event/mailbox contract grounding.
- Additive identity field alignment to UUIDv7 doctrine examples.

## Future idea / not yet implemented
- Production-wide runtime wiring and guaranteed delivery/replay semantics.
- Lobster/llm-task expansion after grounding stabilizes.
