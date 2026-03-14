# ADR-004: Delivery receipt vs acknowledgement separation

## Status
Proposed

## Context
Delivery and processing are different lifecycle milestones.

## Decision
- Delivery receipt captures courier-level delivery observation.
- Acknowledgement captures downstream acceptance/rejection of processing.
- `receipt_id` and `ack_id` are always distinct concrete UUID7 values.

## Consequences
- Distinguishes transport success from workflow completion.
- Supports retries, escalation, and missing-receipt diagnostics.
