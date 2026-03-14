# ADR-003: UUID7 concrete identity strategy

## Status
Proposed

## Context
Comms lifecycle events require both grouping semantics and chronological concrete identity.

## Decision
- Keep umbrella semantic IDs separate from concrete IDs.
- Semantic IDs: `project_id`, `comms_thread_id`.
- Concrete UUID7 IDs: `task_id` or `work_id`, `envelope_id`, `event_id`, `receipt_id`, `ack_id`, `trace_id`.
- Do not overload one ID for both semantic grouping and concrete chronology.

## Consequences
- Replay and lineage remain deterministic.
- Related events can share one `comms_thread_id` while retaining distinct concrete IDs.
