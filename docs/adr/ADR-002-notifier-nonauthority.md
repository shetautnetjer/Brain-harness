# ADR-002: Notifier channels are non-authoritative

## Status
Proposed

## Context
Notification mechanisms are useful for latency and wakeups but unreliable as a source of truth.

## Implemented and tested grounding
- `schemas/notifier_event.schema.json` fixes notifier records as `authoritative: false` and includes `check_authoritative_state` in hint payload discipline.
- `tests/comms/test_comms_contracts.py` verifies notifier records are non-authoritative and reference authoritative stores (`mailbox`, `event-history`, `receipt-ledger`, `ack-ledger`).

## Decision (doctrine)
- `notifier_event` records must remain non-authoritative.
- Notifier payloads must include an instruction to check authoritative state.
- A notifier message may reference IDs (`comms_thread_id`, `envelope_id`, `event_id`) but may not be treated as delivery truth.

## Migration target
- Add runtime inventory checks that show notifier-triggered flows consistently reconcile against authoritative records.

## Future idea / not yet implemented
- Runtime activation of additional notifier transports should be treated as future until proved by runtime inventory and tests.

## Consequences
- Prevents duplicate competing transport buses.
- Enables fs-watch/session ping/polling fallback without changing truth model.
