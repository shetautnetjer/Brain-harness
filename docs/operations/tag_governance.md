# Tag Governance

`main` proposes tags for operational use; `arbiter` governs canonical admission.

- Plane A admits canonical tags and governed `pending/*` tags.
- Plane A stages unknown tags to pending review and emits taxonomy violations.
- Plane B only admits canonical tags (or aliases that resolve to canonical tags) and rejects unknown or plane-disallowed tags.
- Current identity/role vocabulary is intentionally stabilized for two active actors: `identity/main`, `identity/arbiter`, `role/orchestrator`, and `role/governance`.
- Lobster substrate tags remain intentionally pending (`workflow-substrate/lobster` and `comms/lobster-adapter`) until runtime wiring is real and governed.
- Required comms tag bundles by record type are defined in `docs/operations/comms_tag_bundles.md`.
