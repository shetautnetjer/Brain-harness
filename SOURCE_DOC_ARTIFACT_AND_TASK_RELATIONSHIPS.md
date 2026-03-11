# Document, Artifact, and Task Relationships

## Verified in contracts/code
- `doc_id` is human-readable and normalized.
- `chunk_id` is deterministic from `doc_id` + chunk index.
- Ingest contract tracks normalized model alignment targets (`documents`, `document_tags`, `document_aliases`, `document_chunks`, `replay_artifact_links`).

## Migration target
- Broader linking between event/task/artifact envelopes is only partially represented; keep relation guidance additive and file-grounded.
- Avoid introducing abstract relationship layers not evidenced in contracts/scripts/tests.
