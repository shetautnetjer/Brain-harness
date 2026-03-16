# ADR-004: Delivery receipt vs acknowledgement separation

## Status
Proposed

## Context
Delivery and processing are different lifecycle milestones.

## Implemented and tested grounding
- `schemas/delivery_receipt.schema.json` and `schemas/acknowledgement.schema.json` model distinct record types/scopes.
- `tests/comms/test_comms_contracts.py` asserts that receipt records carry `receipt_id` (not `ack_id`) and acknowledgement records carry `ack_id` (not `receipt_id`).

## Decision (doctrine)
- Delivery receipt captures courier-level delivery observation.
- Acknowledgement captures downstream acceptance/rejection of processing.
- `receipt_id` and `ack_id` are always distinct concrete UUID7 values.
- Delivery success is not equivalent to work acceptance or completion.

## Migration target
- Add runtime evidence showing how receipt and acknowledgement states are observed/reconciled in live operations.

## Future idea / not yet implemented
- Any runtime guarantee semantics for receipt/ack timing, completeness, or SLA behavior.

## Consequences
- Distinguishes transport success from workflow completion.
- Supports retries, escalation, and missing-receipt diagnostics.
