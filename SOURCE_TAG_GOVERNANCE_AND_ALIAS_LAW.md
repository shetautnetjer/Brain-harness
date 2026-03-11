# Tag Governance and Alias Law

## Verified in code/contracts
- Canonical tags + aliases are registry-managed (`registries/tag_registry.yaml`).
- Alias resolution is required.
- Unknown tags are staged on Plane A and rejected on Plane B with structured violations; silent drop is forbidden.

## Settled doctrine alignment
- Plane B admits only approved canonical or alias-resolved tags.
- Plane A may stage pending tags.
- Unknown/path-derived junk tags should be rejected or staged per enforcement rules.

## Caveat
- Preservation of rejected tag artifacts for later analytics can be done as data retention practice, but RL/training wiring is not evidenced in repo.
