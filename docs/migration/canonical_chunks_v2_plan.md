# canonical_chunks_v2 migration plan

## Legacy policy
- `canonical_chunks` is **legacy and read-only** during migration.
- New writes must target `canonical_chunks_v2` only.

## Target schema intent
`canonical_chunks_v2` must include:
- deterministic identity (`chunk_id`, normalized `doc_id`, `chunk_index`)
- canonical tags and alias metadata (`canonical_tags_json`, `aliases_json`)
- source linkage (`source_events_json`, `promotion_packet_id`)
- required embedding provenance (`embedding_model`, `embedding_dim`, `source_plane`, `ingest_run_id`, `indexed_at`)

## Rollout
1. Create `canonical_chunks_v2` using explicit DDL from `scripts/migrate_canonical_chunks_v2.py`.
2. Backfill from legacy table with normalization + provenance carry-forward.
3. Run validation checks for missing provenance and mixed planes.
4. Cut writes to v2; keep legacy table for read-only rollback window.

## TODO
- Add transaction-safe migration runner and per-row error quarantine table.
