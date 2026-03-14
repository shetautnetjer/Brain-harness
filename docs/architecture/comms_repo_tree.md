# Proposed communications subsystem tree

Status: Proposed scaffold

```text
contracts/
  comms/
    README.md
registries/
  tag_registry.comms.yaml
schemas/
  comms_identity.schema.json
  envelope.schema.json
  delivery_receipt.schema.json
  acknowledgement.schema.json
  notifier_event.schema.json
docs/
  adr/
    ADR-001-mailbox-authority.md
    ADR-002-notifier-nonauthority.md
    ADR-003-uuid7-identity-strategy.md
    ADR-004-receipt-vs-ack.md
    ADR-005-replay-spine.md
    ADR-006-lobster-pending-compatibility.md
examples/
  comms/
    envelope.example.json
    delivery_receipt.example.json
    acknowledgement.example.json
    notifier_event.example.json
tests/
  comms/
    test_comms_contracts.py
```

This scaffold keeps authoritative records separate from derived notifier hints.
