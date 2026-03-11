# Event Identity and Timeline

## Verified in code/contracts/tests
- Event IDs are generated with UUIDv7 (`make_event_id`) and tested for version/variant shape and uniqueness.
- Identity contract declares UUIDv7 provenance spine fields and deterministic chunk identity.

## Settled doctrine
- UUIDv7 is operational identity/timeline ordering only.
- UUIDv7 must not carry semantic meaning.
- Semantic meaning must come from governed fields (`doc_id`, `chunk_id`, `event_type`, tags, plane, etc.).

## Migration target
- Align identity field names toward doctrine set (`event_id`, `env_id`, `trace_id`, `conversation_id`, `turn_id`, `work_task_id`, `artifact_id`, `promotion_packet_id`, `ingest_run_id`) without breaking existing contract compatibility.
- Current contract uses `session_id`, `envelope_id`, `episode_id`, `work_item_id`; treat this as current state requiring additive migration notes, not forced replacement.
