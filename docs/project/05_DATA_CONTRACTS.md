# 05 — Data Contracts

## Verified in code
- Contracts exist for ingest, identity, plane separation, provenance, retrieval, and tags.
- Comms JSON schemas are present for `comms_identity`, `envelope`, `delivery_receipt`, `acknowledgement`, and `notifier_event`.
- Identity contract uses UUIDv7 provenance spine and semantic `doc_id`/deterministic `chunk_id` for core ingest identity.

## Verified in tests
- `tests/comms/test_comms_contracts.py` validates authority-scope separation and UUIDv7 concrete ID shape across comms example records.
- The same suite validates required comms tag bundle expectations for envelope/receipt/ack/notifier records.
- `tests/test_schema_contracts.py` validates machine-readable contract files and ingest alignment tables.

## Verified in runtime inventory
- Runtime inventory artifacts in-repo are examples/seeds, not discovered proof of live contract enforcement.

## Settled doctrine
- Preserve Plane A vs Plane B separation.
- Kimi as sole Plane B writer remains doctrine/planning constraint, not claimed runtime-enforced exclusivity without direct proof.

## Migration target
1. Keep current contract fields as implementation truth while documenting additive naming alignment where doctrine differs.
2. Ground envelope/receipt/ack/replay/promotion semantics in runtime evidence before promoting beyond schema/test level.
3. Keep contract evolution additive and non-breaking.

## Future idea / not yet implemented
- Guarantee-level delivery, receipt, acknowledgement, replay, and promotion semantics in runtime.
- Active Lobster runtime integration for comms workflow execution.

## Doctrine notes / non-overclaim guardrails
- Schema/test presence is implementation evidence for shape and separation, not proof of end-to-end runtime guarantees.
- Do not claim guaranteed delivery, guaranteed receipt, guaranteed acknowledgement, guaranteed replay, or guaranteed promotion from schema presence alone.
- Do not redesign schemas or registries in this pass.
