# ADR-005: Append-only replay spine

## Status
Proposed

## Context
The comms subsystem must support auditability and deterministic reconstruction.

## Implemented and tested grounding
- Schemas and examples include UUIDv7 `event_id` fields on comms records.
- Tag registries/tests include append-only and replay-related doctrine tags (for example `event/append-only`, `event/replayable`).

## Decision (doctrine)
- Every meaningful transition should be representable as an append-only event with UUID7 `event_id`.
- Envelopes, receipts, and acknowledgements remain materialized authoritative record concepts.
- Event history is the intended replay/audit spine.

## Migration target
- Add runtime inventory and verification evidence that replay pathways are wired and operational.
- Keep replay claims conservative until runtime proof exists.

## Future idea / not yet implemented
- Guaranteed replay completeness and deterministic rebuild guarantees in active runtime.

## Consequences
- Timeline reconstruction does not depend on transient notifier paths.
- Violations and policy checks can run from event history doctrine once runtime wiring is proven.
