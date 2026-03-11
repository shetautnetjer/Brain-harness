# Event Append Log and Replay Rules

## Verified evidence
- Ingest contract references `replay_artifact_links` as a target alignment table.
- No concrete append-log engine or replay guarantee implementation is proven in committed runtime code.

## Doctrine/migration guidance
- Treat event append-log + replay semantics as migration targets until a concrete schema + validators + tests are committed.
- Do not claim deterministic replay guarantees without implementation proof.
