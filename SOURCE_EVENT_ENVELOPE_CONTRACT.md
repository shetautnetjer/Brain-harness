# Event Envelope Contract

## Verified in code/contracts/tests
- `event_id` shape is validated by tests.
- Violation records in `src/brain_harness/models.py` define `event_type`, severity, message, context, timestamp.

## Partial / migration target
- No full envelope schema contract file currently defines delivery envelope fields, receipt fields, or mailbox transition semantics.
- `identity_contract.yaml` references `envelope_id`, but no repository-wide enforced envelope object contract is present.

## Doctrine guidance
- Treat envelope/event docs as guidance unless implementation proof exists.
- Keep envelope fields additive and avoid claiming delivery guarantees before runtime evidence exists.
