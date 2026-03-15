# Tag Governance

`main` proposes tags for operational use; `arbiter` governs canonical admission.

- Plane A admits canonical tags and governed `pending/*` tags.
- Plane A stages unknown tags to pending review and emits taxonomy violations.
- Plane B only admits canonical tags (or aliases that resolve to canonical tags) and rejects unknown or plane-disallowed tags.
- Current identity/role vocabulary is intentionally stabilized for two active actors: `identity/main`, `identity/arbiter`, `role/orchestrator`, and `role/governance`.
- Lobster substrate tags remain intentionally pending (`workflow-substrate/lobster` and `comms/lobster-adapter`) until runtime wiring is real and governed.
- Required comms tag bundles by record type are defined in `docs/operations/comms_tag_bundles.md`.

## Registry authority and supplemental views

- Current validator-facing canonical truth is `registries/tag_registry.yaml`.
- If a tag must validate today, it must exist in `registries/tag_registry.yaml`.
- Domain registries (for example `registries/tag_registry.comms.yaml`) are supplemental domain views in current behavior and must not be treated as independent validator truth.

## Future migration note (not implemented in this pass)

Composed multi-registry validator truth is a future option only after explicit ratification and implementation of:
- composition rules,
- precedence rules,
- duplicate/conflict detection,
- normalized metadata,
- validator support,
- tests proving merged behavior.
