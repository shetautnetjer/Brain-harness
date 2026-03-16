# 06 — Active TODO

## Verified in code
- Comms schema scaffolding and examples are landed.
- Retrieval routing, validator flow, and migration starter scripts are present.

## Verified in tests
- Comms contract tests verify schema/example shape discipline and required tag-family expectations.
- Tests do not currently prove guaranteed delivery, guaranteed receipt, guaranteed acknowledgement, guaranteed replay, guaranteed promotion, or active Lobster runtime wiring.

## Verified in runtime inventory
- Inventory artifacts remain example-state; they are not committed discovered snapshots of live runtime behavior.

## Settled doctrine
- Preserve Plane A vs Plane B separation.
- Kimi is sole Plane B writer as doctrine; do not present as runtime-enforced unless proven in code/runtime evidence.

## Now (safe alignment)
1. Keep mail/event/envelope/identity docs aligned to implemented schemas/tests (docs-first, no runtime redesign).
2. Keep comms tag-bundle docs aligned to currently tested/registered families.
3. Add lightweight runtime-inventory refresh process so discovered snapshots can be committed as evidence.
4. Dry-run canonical chunk migration with non-destructive checks.

## Migration target
- Convert example runtime inventory to discovered, periodically refreshed snapshots.
- Add explicit runtime verification checks for delivery/receipt/ack/replay/promotion behavior before making guarantee claims.

## Future idea / not yet implemented
- Broad runtime wiring/integration expansion.
- Event spine v2 cutover.
- Lobster/llm-task runtime integration.

## Explicit non-claims to preserve
- No guaranteed delivery claim.
- No guaranteed receipt claim.
- No guaranteed acknowledgement claim.
- No guaranteed replay claim.
- No guaranteed promotion claim.
- No active Lobster runtime integration claim.
