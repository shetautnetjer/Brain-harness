# ADR-001: Mailbox authority boundary

## Status
Proposed

## Context
The comms subsystem must preserve a single authoritative transport truth and avoid introducing a second authoritative bus.

## Decision
- Authoritative records are mailbox envelopes, delivery receipts, acknowledgements, and append-only event history.
- Notification channels are derived wakeup hints only.
- SQL is used as registry/join surface and must not override authored records.
- Vector indexes are retrieval indexes and must not be treated as authored truth.
- Consumers must verify authoritative state before claiming delivery/ack outcomes.

## Consequences
- Simpler replay and audit behavior.
- No hidden state in UI/session channels.
- Local-first behavior remains robust when notifier channels drop events.
