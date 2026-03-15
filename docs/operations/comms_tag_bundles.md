# Comms Tag Bundles by Record Type

This document defines **minimum required tag bundles** for communications records.
It is intentionally small and operational, so governance/review can quickly reject
under-tagged records.

## Envelope

Required minimum tags:

- one transport tag: `comms/mailbox`
- one event tag: `event/envelope`
- one workflow tag: one of `workflow/handoff`, `workflow/escalate`, or `workflow/retry`
- one project or domain tag when applicable
- one work tag when linked to a task

Recommended:

- `comms/agent-route`
- `comms/work-item-link`
- `comms/envelope-lineage`

## Delivery receipt

Required minimum tags:

- `comms/receipt`
- `comms/delivery-attempt`
- `policy/receipt-required`

Conditional:

- `comms/delivery-failure` when failed
- `comms/redelivery` when retry path begins
- `comms/receipt-missing` for diagnostics

## Acknowledgement

Required minimum tags:

- `comms/ack`
- `policy/ack-distinct-from-receipt`

Conditional:

- `work/completed`
- `work/blocked`
- `work/failed`

## Notifier event

Required minimum tags:

- `comms/notifier`
- `comms/notification-hint`
- `comms/check-authoritative-state`
- `policy/notifier-nonauthoritative`

Conditional:

- `comms/fs-watch`
- `comms/session-ping`
- `comms/polling-fallback`

## Governance notes

- Keep Lobster-related tags pending (`workflow-substrate/lobster`, `comms/lobster-adapter`)
  until there is real runtime wiring.
- Do not create duplicate canonical umbrella families (for example, do not add `mailbox/*`
  if `comms/*` is canonical).
- Transport tags do not replace semantic/project/work tags.
- Tags do not replace governed identity fields like `project_id` and `comms_thread_id`.
