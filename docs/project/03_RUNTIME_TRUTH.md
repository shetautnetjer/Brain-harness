# 03 — Runtime Truth (Verified Only)

## Verified in repository code/manifests
- Agent identity seed includes `main` with root `/home/netjer/.openclaw/workspace` in `scripts/collect_agent_state.py` and `manifests/agents/main.example.yaml`.
- Shared operational workspace seed is `/home/netjer/.openclaw/workspace`.
- Additional named agents in example/runtime seeds: `arbiter`, `haiku`, `jabari`, `tariq`, `kimi`, `heru`.
- Mailbox path convention seed: `/home/netjer/.openclaw/workspace/plane-a/mailbox/agents/<agent>/{inbox,outbox,received}`.
- SQLite path surface seed: `/home/netjer/.openclaw/memory/*.sqlite` and enumerated per-agent sqlite file paths in runtime example snapshot.
- Retrieval adapters are implemented for deterministic local SQLite scanning and optional Plane B metadata lookup against `canonical_chunks_v2`.

## Important reality flags
- Runtime manifests and snapshots are explicitly marked `example` / known-path-not-verified.
- `collect_agent_state.py` reports discovered existence booleans and discovered sqlite paths, but no committed discovered snapshot is present here.
- Plane B metadata retrieval adapter exists, but router warns that registry adapter wiring is TODO/partial.
- Vector fallback is declared in route plan but live LanceDB wiring is TODO.

## Authored truth locations (verified)
- Contracts and registries under `contracts/` and `registries/`.
- Validation logic under `plugins/*_guard` and tests under `tests/`.

## Known uncertainty
- No committed evidence in this repo proving live mailbox health, live sqlite population, or production-grade retrieval orchestration.
- No committed evidence proving full canonical chunk migration completion.
