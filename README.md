# brain-harness

`brain-harness` is a governance + retrieval enforcement harness for an OpenClaw multi-agent memory runtime.

## Purpose
This repository provides guardrails at ingest and retrieval boundaries so runtime behavior can be validated and audited deterministically.

### In scope
- Enforces doctrine in code at ingestion and retrieval boundaries.
- Preserves UUID provenance fields while keeping human-readable `doc_id` fields.
- Keeps Plane A and Plane B isolated in policy and validation.
- Implements deterministic-first retrieval routing (vector search is fallback only).
- Emits structured JSONL violations instead of silently dropping invalid records.

### Out of scope (for now)
- Fully wired production database adapters.
- End-to-end runtime orchestration.

## Installation
```bash
pip install -e .[dev]
```

## Quick verification
```bash
pytest -q
```

## CLI entry points
The package exposes these commands after installation:

- `brain-validate-qmd`
- `brain-validate-tags`
- `brain-validate-provenance`
- `brain-retrieve`

Equivalent script-based entry points are also available:

```bash
python scripts/validate_qmd.py path/to/doc.qmd --plane plane_a
python scripts/validate_tags.py --plane plane_b memory doctrine
python scripts/validate_provenance.py payload.json
python scripts/collect_agent_state.py
```

## Runtime inventory realism
Example manifests under `manifests/runtime/` are intentionally marked as `example` state.
Discovered runtime state should be produced via `scripts/collect_agent_state.py`, which reports known paths plus discovered existence checks.

Known path seeds include:
- `/home/netjer/.openclaw/workspace`
- `/home/netjer/.openclaw/workspace-jabari`
- `/home/netjer/.openclaw/workspace-tariq`
- `/home/netjer/.openclaw/workspace-kimi`
- `/home/netjer/.openclaw/workspace-heru`
- `/home/netjer/.openclaw/workspace-haiku`
- `/home/netjer/.openclaw/workspace-arbiter`
- `/home/netjer/.openclaw/memory/*.sqlite`
- `/home/netjer/.openclaw/workspace/plane-a/mailbox/agents/<agent>/{inbox,outbox,received}/`

## Repository map
- `contracts/`: schema contracts for ingest, identity, provenance, plane, retrieval, and tags.
- `plugins/`: guard and routing plugin implementations + CLI wrappers.
- `scripts/`: utility and validation scripts used in operations and migration.
- `manifests/`: example agent, memory, and runtime manifests.
- `docs/`: architecture, operations, and migration notes.
- `tests/`: pytest suite for contract and routing enforcement behavior.

## Current TODO boundaries
- Replace UUID fallback helper with a true UUIDv7 implementation in runtime.
- Implement production-grade SQLite/LanceDB adapters.
- Add transaction-safe migration execution for `canonical_chunks_v2`.
