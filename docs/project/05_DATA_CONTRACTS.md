# 05 — Data Contracts

## Current-state read
- Contracts exist for ingest, identity, plane separation, provenance, retrieval, and tags.
- Identity contract uses UUIDv7 provenance spine and semantic `doc_id`/deterministic `chunk_id`.
- Envelope/receipt/state-machine contracts are only partial in current implementation.

## Gap list
1. Envelope-specific schema contract is not fully implemented as an enforced runtime object.
2. Receipt/ack guarantees are not implemented/proven.
3. Replay guarantees are not implemented/proven.
4. Identity naming doctrine and current contract fields differ in places.

## Smallest safe patch plan
- Preserve current contract fields as implementation truth.
- Document additive migration guidance for identity naming alignment.
- Keep envelope/receipt/replay items explicitly marked migration target.

## Exact files to edit
- `docs/project/05_DATA_CONTRACTS.md`
- `docs/project/06_ACTIVE_TODO.md`
- `SOURCE_03_DATA_CONTRACTS_AND_MIGRATION.md`
- `docs/project/07_EVENT_AND_MAIL_ALIGNMENT.md`

## Validation steps / tests
- Run `pytest -q`.
- Confirm docs only; no runtime behavior change.

## Doctrine risks / drift risks
- Overclaiming delivery/receipt/replay guarantees would conflict with repo evidence.
- Replacing current identity fields non-additively would violate migration doctrine.
