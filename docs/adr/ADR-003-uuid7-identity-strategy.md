# ADR-003: UUID7 concrete identity strategy

## Status
Proposed

## Context
Comms lifecycle events require both grouping semantics and chronological concrete identity.

## Implemented and tested grounding
- `schemas/comms_identity.schema.json` enforces separation of semantic identity (`project_id`, `comms_thread_id`) and concrete identity (`trace_id`).
- Envelope/receipt/ack schemas model distinct UUIDv7 concrete IDs for their own records (`envelope_id`, `receipt_id`, `ack_id`) and associated `event_id` values.
- `tests/comms/test_comms_contracts.py` checks UUIDv7 shape across these concrete IDs and checks shared `comms_thread_id` continuity across related records.

## Decision (doctrine)
- Keep umbrella semantic IDs separate from concrete IDs.
- Semantic IDs: `project_id`, `comms_thread_id`.
- Concrete IDs currently grounded in comms schemas: `trace_id`, `event_id`, `envelope_id`, `receipt_id`, `ack_id`.
- Do not overload one ID for both semantic grouping and concrete chronology.

## Migration target
- Keep additive alignment work between broader identity naming doctrine and implemented field names without non-additive breakage.

## Future idea / not yet implemented
- Broader identity harmonization beyond currently committed schemas, if later proven useful.

## Consequences
- Replay and lineage remain deterministic at the schema/test level.
- Related events can share one `comms_thread_id` while retaining distinct concrete IDs.
