# SOURCE 01 — Mission, Runtime, and Planes

## Mission (repo-grounded)
Brain Harness is a governance + retrieval enforcement harness around OpenClaw multi-agent memory workflows, with deterministic guardrails at ingest/retrieval boundaries and audit-friendly violation output. This is explicitly stated in repository README, contracts, plugins, and tests.

## Plane doctrine (settled)
- **Plane A**: working / staging / operational surface (provisional, local, evolving).
- **Plane B**: canonical / promoted / curated shared surface.
- **Separation is mandatory** (mixed embedding stores are forbidden by contract).
- **Kimi is the sole Plane B writer** (settled project doctrine for this run).

## Verified implementation signals
- Plane role separation is defined in `contracts/plane_contract.yaml`.
- QMD validation has Plane-specific required fields in `registries/doc_type_rules.yaml` and `plugins/qmd_guard/validator.py`.
- Retrieval logic treats `canonical_truth` as local-first with conditional Plane B escalation in `plugins/retrieval_router/router.py`.

## Doctrine vs implementation disclaimer
Items like “Kimi sole Plane B writer” and some authority boundaries are doctrine in this pass unless/until enforced by runtime write ACL code. They must still be preserved as project rules.
