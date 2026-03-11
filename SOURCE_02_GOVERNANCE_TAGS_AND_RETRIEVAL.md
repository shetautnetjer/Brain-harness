# SOURCE 02 — Governance, Tags, and Retrieval

## Governance summary
- Arbiter has final authority over doctrine/taxonomy admission and violation classes (settled doctrine).
- Tag governance is contract-backed: unknown tags are staged on Plane A and rejected on Plane B with emitted violations.
- Silent drops are forbidden.

## Tag/taxonomy principles
- Canonical tags + aliases live in `registries/tag_registry.yaml`.
- Validation resolves aliases to canonical tags.
- Pending tags are staged to `registries/pending_tags.jsonl` for Plane A.

## Retrieval principles
- Deterministic-first retrieval is encoded in contract and router behavior.
- Query classifier picks an intent; router executes deterministic local SQL pathways first.
- `canonical_truth` intent checks local references first, then conditionally escalates to Plane B metadata.
- Vector search is fallback/index behavior only; current code marks live LanceDB wiring as TODO.

## Evidence standards
- Files/SQL/registry-backed retrieval is primary.
- Vector/index layers are acceleration aids, not authored truth.
- If a behavior is not evidenced in code/contracts/tests/manifests/scripts, mark it as migration target or future idea.
