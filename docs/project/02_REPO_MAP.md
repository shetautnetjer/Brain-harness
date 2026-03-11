# 02 — Repo Map

## Top-level directories and actual use
- `contracts/`: YAML doctrine/contracts for ingest, identity, planes, provenance, retrieval, tag governance.
- `docs/`: architecture, operations, and migration notes (plus this project state layer).
- `manifests/`:
  - `agents/*.example.yaml`: seeded agent roots/mailboxes (example state).
  - `memory/*.example.yaml`: seeded plane/store role metadata.
  - `runtime/*.example.*`: seeded runtime inventory/system manifests.
- `plugins/`:
  - `qmd_guard`: frontmatter and doc_type gate enforcement.
  - `tag_guard`: taxonomy validation, alias normalization, violation/pending emission.
  - `provenance_guard`: provenance and plane-separation validation.
  - `plane_router`: simple plane routing helper.
  - `retrieval_router`: query classification + deterministic retrieval adapter routing.
- `prompts/`: role/operator prompts (`arbiter`, `kimi`, `heru`, `inventory`, `codex`).
- `registries/`: `tag_registry.yaml`, `doc_type_rules.yaml`, pending tags JSONL.
- `scripts/`: CLIs/utilities for validation, inventory collection, audits, migration starter, tag listing.
- `src/brain_harness/`: core models/settings/events/jsonl utilities.
- `tests/`: pytest coverage for normalization, contracts readability, provenance, retrieval routing, qmd rules.
- `workflows/`: lobster workflow specs for ingest/retrieve/promote flows.

## Key files to anchor orientation
- `README.md`
- `contracts/retrieval_contract.yaml`
- `contracts/ingest_contract.yaml`
- `plugins/retrieval_router/router.py`
- `plugins/retrieval_router/adapters.py`
- `scripts/collect_agent_state.py`
- `scripts/migrate_canonical_chunks_v2.py`
- `manifests/runtime/inventory_snapshot.example.json`
- `tests/test_retrieval_routing.py`
