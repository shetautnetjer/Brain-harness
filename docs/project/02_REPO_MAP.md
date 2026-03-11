# 02 — Repo Map

## Verified in code
- `contracts/`: ingest/identity/plane/provenance/retrieval/tag contracts.
- `registries/`: canonical tag + alias registry and doc_type rules.
- `plugins/`: qmd/tag/provenance guards plus deterministic retrieval router.
- `scripts/`: validation, runtime inventory collection, audits, canonical chunk migration starter.
- `tests/`: contract, identity, retrieval, provenance, and frontmatter enforcement tests.

## Verified in runtime inventory examples
- `manifests/agents/*.example.yaml`
- `manifests/runtime/*.example.*`

## Doctrine + migration docs
- Core source docs at repository root (`SOURCE_01...SOURCE_04`).
- Envelope/event source docs at repository root (`SOURCE_*ENVELOPE*`, `SOURCE_UUIDV7_USAGE_RULES.md`, etc.).
- Project grounding docs in `docs/project/`.
