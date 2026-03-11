# 00 — Project State

## Mission summary
Brain Harness enforces governance and deterministic retrieval behavior across OpenClaw memory planes, with validation at ingest and retrieval boundaries and explicit violation emission.

## Verified baseline
- Contracts for ingest/identity/plane/provenance/retrieval/tags exist and are machine-readable.
- Guard plugins exist for QMD frontmatter, tags, provenance, plane routing, retrieval routing.
- Retrieval router is deterministic-first and treats vector as fallback with TODO wiring warning.
- Test suite exists and covers key doctrine enforcement points.
- Runtime and agent manifests are **example seeds**, not discovered truth.

## Settled doctrine
- Preserve Plane A / Plane B separation.
- Kimi is sole Plane B writer.
- Arbiter is final authority on doctrine/taxonomy/admission/promotion/violation classes.
- Files are authored truth.
- SQL is registry/join surface.
- Vector stores are indexes, not authored truth.
- Deterministic/file-grounded retrieval first.
- Narrow additive patches only.

## Migration targets
- Transaction-safe `canonical_chunks_v2` migration runner.
- Live adapter wiring for normalized model alignment tables referenced in ingest contract.
- Signed/discovered runtime inventory promotion flow.

## Future ideas / not yet implemented
- Production-grade DB adapter orchestration and full runtime wiring.
- Lobster / llm-task augmentation after baseline grounding is stable.

## Immediate next milestone
Confirm retrieval baseline against deterministic local SQL behavior + conditional Plane B escalation expectations.

## Top known gaps
- Example manifests are not runtime-verified snapshots.
- Plane B adapter wiring is partial and explicitly warns as such.
- Vector store wiring (e.g., LanceDB) remains TODO.
- Canonical chunk migration script is starter-level and not transaction-safe.

## Files every model should inspect first
1. `README.md`
2. `contracts/*.yaml`
3. `plugins/retrieval_router/*.py`
4. `plugins/qmd_guard/validator.py`
5. `plugins/tag_guard/validator.py`
6. `plugins/provenance_guard/validator.py`
7. `scripts/collect_agent_state.py`
8. `scripts/migrate_canonical_chunks_v2.py`
9. `tests/test_retrieval_routing.py`
10. `tests/test_qmd_frontmatter_enforcement.py`
