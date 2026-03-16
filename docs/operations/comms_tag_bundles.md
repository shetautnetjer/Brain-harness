# Comms Tag Bundles by Record Type

This document defines **minimum required tag bundles** for communications records.
It is intentionally small and operational, so governance/review can quickly reject
under-tagged records.

Status markers used below:
- **Verified in tests** = asserted in `tests/comms/test_comms_contracts.py` and backed by current registries/examples.
- **Migration target** = desired runtime enforcement not yet proven in runtime inventory.
- **Future idea** = not currently implemented/proven.

## Envelope

Required minimum tags (**verified in tests**):

- one transport tag: `comms/mailbox`
- one event tag: `event/envelope`
- one workflow tag: one of `workflow/handoff`, `workflow/escalate`, or `workflow/retry`

Conditional:

- project/domain tags when applicable to routing or audit scope
- work tags when linked to a specific task/work item

Recommended:

- `comms/agent-route`
- `comms/work-item-link`
- `comms/envelope-lineage`

## Delivery receipt

Required minimum tags (**verified in tests**):

- `comms/receipt`
- `comms/delivery-attempt`
- `policy/receipt-required`

Conditional (**verified in tests as present in registry**):

- `comms/delivery-failure` when failed
- `comms/redelivery` when retry path begins
- `comms/receipt-missing` for diagnostics

## Acknowledgement

Required minimum tags (**verified in tests**):

- `comms/ack`
- `policy/ack-distinct-from-receipt`

Conditional (**verified in tests as present in registry**):

- `work/completed`
- `work/blocked`
- `work/failed`

## Notifier event

Required minimum tags (**verified in tests**):

- `comms/notifier`
- `comms/notification-hint`
- `comms/check-authoritative-state`
- `policy/notifier-nonauthoritative`

Conditional (**verified in tests as present in registry**):

- `comms/fs-watch`
- `comms/session-ping`
- `comms/polling-fallback`

## Governance notes

- Keep Lobster-related tags pending (`workflow-substrate/lobster`, `comms/lobster-adapter`)
  until there is real runtime wiring.
- Do not create duplicate canonical umbrella families (for example, do not add `mailbox/*`
  if `comms/*` is canonical).
- `comms/inbox` and `comms/outbox` are active tags in registry, but they are not currently asserted as minimum required bundle tags by the comms contract tests/examples.
- Transport tags do not replace semantic/project/work tags.
- Tags do not replace governed identity fields like `project_id` and `comms_thread_id`.

## Runtime claim boundaries

- **Verified in code/tests:** schema/test coverage exists for record/tag shape and authority-scope separation.
- **Verified in runtime inventory:** not yet; committed inventory artifacts are examples.
- **Migration target:** runtime checks that prove whether expected receipt/ack/retry pathways occur in practice.
- **Future idea:** any guarantee-level runtime semantics (delivery/receipt/ack/replay/promotion) and active Lobster transport integration.
