# ADR-006: Lobster compatibility is pending substrate work

## Status
Proposed (pending)

## Context
The project wants future Lobster compatibility but should not present it as ratified doctrine prematurely.

## Implemented and tested grounding
- `workflow-substrate/lobster` and `comms/lobster-adapter` tags exist and are validated as pending in comms contract tests.

## Decision (doctrine)
- Keep `workflow-substrate/lobster` and `comms/lobster-adapter` tags in pending state.
- Do not claim active Lobster runtime integration in code.
- Maintain schema and contract surface neutral enough to map into a future adapter.

## Migration target
- Define/runtime-prove integration boundaries before changing pending status.

## Future idea / not yet implemented
- Active Lobster-backed runtime adapter and operational workflow execution.

## Consequences
- Honest status signaling.
- Lower migration risk when substrate doctrine is ratified.
