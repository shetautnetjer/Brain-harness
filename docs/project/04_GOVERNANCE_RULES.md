# 04 — Governance Rules

## Settled doctrine
1. Preserve Plane A vs Plane B separation.
2. Kimi is sole Plane B writer.
3. Arbiter is final authority on doctrine/taxonomy/admission/promotion/violation classes.
4. Files are authored truth.
5. SQL is registry/join surface.
6. Vector stores are indexes, not authored truth.
7. Prefer deterministic/file-grounded retrieval first.
8. Keep patches narrow and additive.
9. Prefer additive migration over silent semantic replacement.
10. Do not invent runtime behavior not evidenced by repo files.

## Tag registry authority (current-state law)
11. `registries/tag_registry.yaml` is the authored canonical validator-facing tag registry.
12. Domain-specific tag files (for example, comms-focused registries) are supplemental domain views unless and until explicit composed multi-registry law is ratified and implemented.
13. If a tag must validate in current runtime behavior, it must be present in `registries/tag_registry.yaml`.

## Future composition migration guardrails (not yet active)
- Any multi-registry validator truth requires explicit composition rules, precedence rules, duplicate/conflict detection, normalized metadata, validator support, and tests proving merged behavior.

## Verified enforcement loci in code
- `plugins/qmd_guard/validator.py`
- `plugins/tag_guard/validator.py`
- `plugins/provenance_guard/validator.py`
- `plugins/retrieval_router/router.py`
