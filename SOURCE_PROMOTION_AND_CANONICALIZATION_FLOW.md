# Promotion and Canonicalization Flow

## Verified in docs/contracts/scripts
- Promotion concept exists in operations docs and ingest doc_type rules (`source_events` requirements for promoted/canonical contexts).
- `canonical_chunks_v2` migration starter script and migration docs exist.

## Partial implementation status
- Migration tooling is starter-level with explicit TODOs for transaction-safe cutover.
- No proof here of complete production promotion pipeline.

## Doctrine
- Keep operational mail/event flow separate from canonical promotion flow.
- Use additive migration, not silent semantic replacement.
