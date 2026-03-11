# Message Lifecycle and State Machine

## Verified in repository
- Mailbox directory pattern is seeded (`inbox`, `outbox`, `received`) in manifests and runtime inventory scripts/examples.

## Not verified
- No committed state-machine implementation proving full lifecycle transitions, retries, dead-letter handling, or replay queues.

## Migration target
- Define lifecycle transitions as explicit contract states only after corresponding code/tests are added.
- Until then, treat lifecycle model as doctrine guidance only.
