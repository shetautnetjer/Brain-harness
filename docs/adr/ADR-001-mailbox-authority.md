# ADR-001: Mailbox authority boundary

## Status
Proposed

## Context
The comms subsystem must preserve a single authoritative transport truth and avoid introducing a second authoritative bus.

## Implemented and tested grounding
- Comms schemas and examples model envelope/receipt/ack as authoritative records and notifier as non-authoritative.
- `tests/comms/test_comms_contracts.py` checks authority-scope separation and notifier discipline.

## Decision (doctrine)
- Authoritative record concepts are mailbox envelopes, delivery receipts, acknowledgements, and append-only event history.
- Notification channels are derived wakeup hints only.
- SQL is registry/join surface and must not override authored records.
- Vector indexes are retrieval indexes and must not be treated as authored truth.
- Consumers must verify authoritative state before claiming delivery/ack outcomes.

## Migration target
- Strengthen runtime inventory evidence for mailbox/event-history/ledger health.

## Future idea / not yet implemented
- End-to-end guaranteed mailbox delivery/receipt/ack/replay semantics.

## Consequences
- Simpler replay and audit behavior.
- No hidden state in UI/session channels.
- Local-first behavior remains robust when notifier channels drop events.
