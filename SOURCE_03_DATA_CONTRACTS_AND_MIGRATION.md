# SOURCE 03 — Data Contracts and Migration

## Authored truth and registry expectations
- Authored truth is file-grounded (QMD/docs/contracts/registries/manifests) and validated at boundaries.
- SQL surfaces act as registry/join/query substrates, not freeform truth replacement.
- Expected entities include docs/chunks/tags/aliases/provenance/event links as represented in contracts and migration DDL targets.

## Contract-backed expectations
- Identity contract: UUIDv7 provenance spine + human-readable normalized `doc_id` + deterministic `chunk_id`.
- Ingest contract: frontmatter choke-point and plane/doc_type rules.
- Tag contract: alias resolution required; Plane A stage pending, Plane B reject unknown.
- Provenance contract: required embedding provenance fields and plane-mixing prohibition.
- Retrieval contract: deterministic-first, classifier required, vector not first step.

## Migration philosophy
- Prefer additive migration paths over silent replacement.
- Keep legacy surfaces readable during migration windows.
- Explicitly validate provenance and plane separation before cutover.
- Do not claim migration completion without code/tests/runtime evidence.

## Current migration target in repo
- `canonical_chunks_v2` exists as planned DDL + transform helpers in migration script.
- Transaction-safe backfill/writer cutover remains TODO and must be treated as incomplete.
