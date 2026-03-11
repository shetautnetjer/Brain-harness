# Runtime inventory doctrine

- Files under `manifests/runtime/*.example.*` are **seed examples**, not live discovery output.
- Live discovery should come from `scripts/collect_agent_state.py` and explicitly mark discovered vs known-example values.

## Seeded known paths (from runtime facts)
- Agent roots:
  - `/home/netjer/.openclaw/workspace`
  - `/home/netjer/.openclaw/workspace-jabari`
  - `/home/netjer/.openclaw/workspace-tariq`
  - `/home/netjer/.openclaw/workspace-kimi`
  - `/home/netjer/.openclaw/workspace-heru`
  - `/home/netjer/.openclaw/workspace-haiku`
  - `/home/netjer/.openclaw/workspace-arbiter`
- SQLite glob: `/home/netjer/.openclaw/memory/*.sqlite`
- Mailboxes: `/home/netjer/.openclaw/workspace/plane-a/mailbox/agents/<agent>/{inbox,outbox,received}/`

## TODO
- Add a signed inventory snapshot flow so manifests can be promoted from `example` to `discovered` state.
