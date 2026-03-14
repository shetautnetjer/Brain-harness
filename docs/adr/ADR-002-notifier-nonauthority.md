# ADR-002: Notifier channels are non-authoritative

## Status
Proposed

## Context
Notification mechanisms are useful for latency and wakeups but unreliable as a source of truth.

## Decision
- `notifier_event` records must set `authoritative: false`.
- Notifier payloads must include an instruction to check authoritative state.
- A notifier message may reference IDs (`comms_thread_id`, `envelope_id`, `event_id`) but may not be treated as delivery truth.

## Consequences
- Prevents duplicate competing transport buses.
- Enables fs-watch/session ping/polling fallback without changing truth model.
