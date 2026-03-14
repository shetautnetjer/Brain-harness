# ADR-005: Append-only replay spine

## Status
Proposed

## Context
The comms subsystem must support auditability and deterministic reconstruction.

## Decision
- Every meaningful transition is emitted as an append-only event with UUID7 `event_id`.
- Envelopes, receipts, and acknowledgements remain materialized authoritative records.
- Event history is replayable and forms the audit spine.

## Consequences
- Timeline reconstruction does not depend on transient notifier paths.
- Violations and policy checks can run from event history.
