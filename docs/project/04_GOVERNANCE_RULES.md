# 04 — Governance Rules to Preserve

1. Preserve Plane A vs Plane B separation.
2. Kimi is sole Plane B writer (doctrine rule).
3. Arbiter is final authority for doctrine, tag taxonomy, admission/promotion rules, violation classes.
4. Files are authored truth.
5. SQL is registry/join/query surface.
6. Vector stores are indexes, not authored truth.
7. Deterministic/file-grounded retrieval before semantic/vector fallback.
8. Keep patches narrow.
9. Prefer additive migration over silent replacement.
10. Do not invent runtime behavior that is not evidenced by code/contracts/tests/scripts/manifests/fixtures/validators.

## Enforcement loci in code
- QMD ingest frontmatter + tag + doc_type enforcement: `plugins/qmd_guard/validator.py`.
- Tag admission behavior and violation emission: `plugins/tag_guard/validator.py`.
- Provenance/plane separation checks: `plugins/provenance_guard/validator.py`.
- Retrieval routing doctrine: `plugins/retrieval_router/router.py` and `contracts/retrieval_contract.yaml`.
