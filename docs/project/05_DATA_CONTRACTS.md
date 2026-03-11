# 05 — Data Contracts (Plain-English)

## Documents/frontmatter
- Ingest is contract-gated at QMD/frontmatter validation.
- Required fields differ by plane; Plane B has stricter required metadata.
- Doc type rules can add required fields and source event requirements.

## Identity
- Provenance/event spine uses UUIDv7 fields (`event_id`, `trace_id`, etc.).
- `doc_id` is normalized human-readable kebab-case.
- `chunk_id` is deterministic (`doc_id::chunk::<index>`).

## Tags
- Canonical tags and aliases are registry-managed.
- Alias resolution is required.
- Unknown tags:
  - Plane A: stage pending + emit warning violation.
  - Plane B: reject + emit error violation.

## Provenance and vector writes
- Required provenance fields for vector/index writes include model, dim, source_plane, ingest_run_id, indexed_at.
- Mixed planes in one table/batch are forbidden.

## Retrieval results
- Retrieval output contracts include intent, plan, records, citations, vector usage flag, plane escalation flag, warnings.

## Chunks/canonical migration
- `canonical_chunks_v2` target schema and transform behavior exist in migration script and migration docs.
- Full live schema contract for all runtime DB tables is not fully implemented in this repository; treat some tables and adapters as partially wired/TODO.
