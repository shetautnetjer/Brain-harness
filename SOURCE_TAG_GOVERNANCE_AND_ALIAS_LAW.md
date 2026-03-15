# Tag Governance and Alias Law

## Verified in code/contracts
- Canonical tags + aliases are registry-managed (`registries/tag_registry.yaml`).
- Alias resolution is required.
- Unknown tags are staged on Plane A and rejected on Plane B with structured violations; silent drop is forbidden.
- `registries/tag_registry.yaml` is the single authored canonical validator-facing registry in current implementation.
- Domain files such as `registries/tag_registry.comms.yaml` are supplemental/derived views unless explicit multi-registry composition law is ratified and implemented.

## Settled doctrine alignment
- Plane B admits only approved canonical or alias-resolved tags.
- Plane A may stage pending tags.
- Unknown/path-derived junk tags should be rejected or staged per enforcement rules.
- Arbiter remains final authority for taxonomy, admission, and violation governance.
- Supplemental domain registries must not be treated as independent validator truth in the current single-registry model.

## Future migration target (not yet implemented)
- Multi-registry composition is allowed only after explicit ratification and implementation of:
  - composition rules,
  - precedence rules,
  - duplicate/conflict detection,
  - normalized metadata,
  - validator support,
  - tests proving merged behavior.

## Caveat
- Preservation of rejected tag artifacts for later analytics can be done as data retention practice, but RL/training wiring is not evidenced in repo.
