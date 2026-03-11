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

## Verified enforcement loci in code
- `plugins/qmd_guard/validator.py`
- `plugins/tag_guard/validator.py`
- `plugins/provenance_guard/validator.py`
- `plugins/retrieval_router/router.py`
