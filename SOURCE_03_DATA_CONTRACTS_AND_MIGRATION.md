# SOURCE 03 — Data Contracts and Migration

## Current-state read (repo-grounded)
- Contracts exist for ingest, identity, planes, provenance, retrieval, and tags.
- Ingest enforces required frontmatter by plane + doc_type rules, including Plane B source event requirements by default.
- Identity currently mixes UUIDv7 provenance fields with semantic document/chunk identity.
- Migration scaffolding exists for `canonical_chunks_v2`, with explicit TODO for transaction-safe production flow.

## Gap list against doctrine
1. Envelope/event-specific contract files are not fully implemented as runtime-enforced schemas.
2. Identity field names in `contracts/identity_contract.yaml` only partially match doctrine examples.
3. Replay/append-log guarantees are not proven; only alignment targets are named.

## Smallest safe patch plan
- Keep runtime behavior unchanged.
- Document current contracts strictly as implemented truth.
- Mark missing envelope/replay guarantees as migration targets.
- Define additive identity-field migration guidance (no breaking rename claims).

## Exact files to edit
- `SOURCE_03_DATA_CONTRACTS_AND_MIGRATION.md`
- `docs/project/05_DATA_CONTRACTS.md`
- `docs/project/06_ACTIVE_TODO.md`
- `docs/project/07_EVENT_AND_MAIL_ALIGNMENT.md` (new)

## Validation steps
- Verify source docs map to real repository files.
- Run tests to confirm no runtime behavior was changed.

## Doctrine risks / drift risks
- Overstating mailbox or replay guarantees would create doctrine/implementation drift.
- Silent identity renaming would risk breaking external references; use additive migration only.
