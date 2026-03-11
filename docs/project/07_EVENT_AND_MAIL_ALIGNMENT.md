# 07 — Event and Mail Alignment Audit

## Source locations inspected
- `contracts/identity_contract.yaml`
- `src/brain_harness/events.py`
- `src/brain_harness/models.py`
- `scripts/collect_agent_state.py`
- `manifests/runtime/system_manifest.example.yaml`
- `manifests/runtime/inventory_snapshot.example.json`
- `plugins/qmd_guard/validator.py`
- `plugins/tag_guard/validator.py`
- `docs/operations/promotion_flow.md`

## Current behavior found
- Event ID generation is UUIDv7-backed and prefix-based.
- Identity contract includes UUIDv7 provenance fields plus semantic `doc_id` and deterministic `chunk_id`.
- Mailbox routing exists as path conventions in example manifests/inventory seeds.
- No full envelope/receipt/state-machine runtime contract is enforced in code.

## Mismatches against doctrine
- Doctrine sample field names (`env_id`, `conversation_id`, `turn_id`, `artifact_id`, `work_task_id`) are not fully reflected in current identity contract naming.
- Envelope lifecycle and delivery/receipt guarantees are doctrine-level only.

## What should be fixed now
- Keep docs explicit about partial implementation.
- Add additive migration notes for identity field-name alignment.
- Preserve strict non-claims for delivery/receipt/replay/promotion guarantees.

## What should wait until later
- Runtime envelope object and state-machine implementation.
- Guarantee-bearing delivery/receipt/replay infrastructure.
- Broad event spine rewiring.
