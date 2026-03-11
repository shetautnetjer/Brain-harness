# Delivery, Receipt, and Ack Contract

## Verified now
- Mailbox directories include a `received/` path convention in examples.

## Not verified / do not claim
- No code/tests proving delivery guarantee, receipt guarantee, ack SLA, replay guarantee, or promotion guarantee.
- No committed receipt schema contract currently enforces ack payload shape.

## Migration target
- If receipt contracts are added, they should be explicit, append-only, and test-backed.
