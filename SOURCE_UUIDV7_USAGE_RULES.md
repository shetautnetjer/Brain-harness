# UUIDv7 Usage Rules

## Settled doctrine
- Use UUIDv7 for globally unique, time-sortable operational identity and ordering.
- UUIDv7 does not encode business semantics.
- Keep semantic IDs (`doc_id`, deterministic `chunk_id`, governed tags/types) separate.

## Current repo alignment
- UUIDv7 is used and tested for event IDs.
- Identity contract declares UUIDv7 provenance spine.

## Migration target
- Additive alignment of field names with doctrine examples (e.g., `env_id`, `conversation_id`, `turn_id`, `artifact_id`, `work_task_id`) should not break current fields already in contract.
