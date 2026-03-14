# ADR-006: Lobster compatibility is pending substrate work

## Status
Proposed (pending)

## Context
The project wants future Lobster compatibility but should not present it as ratified doctrine prematurely.

## Decision
- Keep `workflow-substrate/lobster` and `comms/lobster-adapter` tags in pending state.
- Do not claim active Lobster runtime integration in code.
- Maintain schema and contract surface neutral enough to map into a future adapter.

## Consequences
- Honest status signaling.
- Lower migration risk when substrate doctrine is ratified.
