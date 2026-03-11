# Agent and Mailbox Routing

## Verified in code/manifests
- Known agent identities include `main`, `arbiter`, `haiku`, `jabari`, `tariq`, `kimi`, `heru` in example manifests/inventory seeds.
- Shared operational workspace root is `/home/netjer/.openclaw/workspace` (example system manifest + collect script seed).
- Mailbox pattern is `/home/netjer/.openclaw/workspace/plane-a/mailbox/agents/<agent>/{inbox,outbox,received}/`.

## Settled doctrine
- Aya identity = `main`.
- Preserve distinction between operational mail/event flow vs canonical promotion flow vs tag governance flow.

## Runtime caveat
- Current repo evidence is example/seeded inventory; mailbox health and runtime delivery are not proven by committed runtime snapshots.
