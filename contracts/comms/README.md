# Communications Contracts (Proposed)

This folder is the proposed contract surface for local-first communications.

## Scope
- `schemas/comms_identity.schema.json`: umbrella semantic IDs vs concrete UUID7 trace identity.
- `schemas/envelope.schema.json`: authoritative mailbox transport record.
- `schemas/delivery_receipt.schema.json`: authoritative delivery fact.
- `schemas/acknowledgement.schema.json`: authoritative acceptance/ownership fact.
- `schemas/notifier_event.schema.json`: derived notifier hint record (non-authoritative).

## Authority discipline
- Authoritative truth: mailbox envelope files, delivery receipt files, acknowledgement files, append-only event history, and promoted Plane B outputs.
- Derived-only hints: fs-watch/session ping/polling/SSE/websocket/local-socket notifier surfaces.
- SQL is a registry/join surface, not authored truth.
- Vector index is an index/retrieval aid, not authored truth.
- Notifier payloads are never transport truth; consumers must re-read authoritative records.
