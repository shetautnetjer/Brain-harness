import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
UUID7_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")


def _load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def _load_schema(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def test_identity_schema_separates_umbrella_and_concrete() -> None:
    schema = _load_schema("schemas/comms_identity.schema.json")
    assert schema["required"] == ["semantic", "concrete"]
    assert set(schema["properties"]["semantic"]["required"]) == {"project_id", "comms_thread_id"}
    assert schema["properties"]["semantic"]["additionalProperties"] is False
    assert schema["properties"]["concrete"]["required"] == ["trace_id"]
    assert schema["properties"]["concrete"]["additionalProperties"] is False


def test_record_scopes_are_strictly_separated() -> None:
    envelope = _load_json("examples/comms/envelope.example.json")
    receipt = _load_json("examples/comms/delivery_receipt.example.json")
    ack = _load_json("examples/comms/acknowledgement.example.json")
    notifier = _load_json("examples/comms/notifier_event.example.json")

    assert envelope["record_type"] == "envelope"
    assert envelope["authority_scope"] == "authoritative-transport-record"
    assert "receipt_id" not in envelope and "ack_id" not in envelope

    assert receipt["record_type"] == "delivery_receipt"
    assert receipt["authority_scope"] == "authoritative-delivery-fact"
    assert "receipt_id" in receipt and "ack_id" not in receipt

    assert ack["record_type"] == "acknowledgement"
    assert ack["authority_scope"] == "authoritative-ownership-fact"
    assert "ack_id" in ack and "receipt_id" not in ack

    assert notifier["record_type"] == "notifier_event"
    assert notifier["authority_scope"] == "derived-notification-hint"
    assert notifier["authoritative"] is False


def test_notifier_is_non_authoritative_hint_only() -> None:
    notifier = _load_json("examples/comms/notifier_event.example.json")

    assert notifier["authoritative"] is False
    assert notifier["hint"]["check_authoritative_state"] is True
    refs = set(notifier["hint"]["authoritative_refs"])
    assert {"mailbox", "event-history", "receipt-ledger", "ack-ledger"}.issubset(refs)


def test_uuid7_required_on_concrete_event_objects() -> None:
    envelope = _load_json("examples/comms/envelope.example.json")
    receipt = _load_json("examples/comms/delivery_receipt.example.json")
    ack = _load_json("examples/comms/acknowledgement.example.json")
    notifier = _load_json("examples/comms/notifier_event.example.json")

    concrete_ids = [
        envelope["envelope_id"],
        envelope["event_id"],
        envelope["identity"]["concrete"]["trace_id"],
        receipt["receipt_id"],
        receipt["event_id"],
        receipt["identity"]["concrete"]["trace_id"],
        ack["ack_id"],
        ack["event_id"],
        ack["identity"]["concrete"]["trace_id"],
        notifier["event_id"],
        notifier["hint"]["event_id"],
    ]
    for value in concrete_ids:
        assert UUID7_RE.match(value), value


def test_comms_thread_id_repeats_across_related_records() -> None:
    envelope = _load_json("examples/comms/envelope.example.json")
    receipt = _load_json("examples/comms/delivery_receipt.example.json")
    ack = _load_json("examples/comms/acknowledgement.example.json")
    notifier = _load_json("examples/comms/notifier_event.example.json")

    thread_id = envelope["identity"]["semantic"]["comms_thread_id"]
    assert receipt["identity"]["semantic"]["comms_thread_id"] == thread_id
    assert ack["identity"]["semantic"]["comms_thread_id"] == thread_id
    assert notifier["hint"]["comms_thread_id"] == thread_id


def test_pending_tags_are_not_active() -> None:
    registry = yaml.safe_load((ROOT / "registries/tag_registry.comms.yaml").read_text())
    tags = {item["canonical_tag"]: item for item in registry["tags"]}

    pending = {
        "workflow-substrate/lobster",
        "comms/lobster-adapter",
        "comms/sse",
        "comms/websocket",
        "comms/local-socket",
    }
    for tag in pending:
        assert tag in tags
        assert tags[tag]["status"] == "pending"


def test_authority_discipline_tags_present() -> None:
    registry = yaml.safe_load((ROOT / "registries/tag_registry.yaml").read_text())
    tags = {item["canonical_tag"]: item for item in registry["tags"]}

    assert tags["policy/notifier-nonauthoritative"]["status"] == "active"
    assert tags["event/append-only"]["status"] == "active"
    assert tags["memory/vector-index-only"]["status"] == "active"


def test_envelope_has_required_transport_and_event_tags() -> None:
    envelope_tags = set(_load_json("examples/comms/envelope.example.json")["tags"])

    assert "comms/mailbox" in envelope_tags
    assert "event/envelope" in envelope_tags
    assert {"workflow/handoff", "workflow/escalate", "workflow/retry"} & envelope_tags


def test_receipt_has_required_receipt_policy_tags() -> None:
    registry = yaml.safe_load((ROOT / "registries/tag_registry.yaml").read_text())
    registry_tags = {item["canonical_tag"] for item in registry["tags"]}
    example_tags = set(_load_json("examples/comms/delivery_receipt.example.json")["tags"])

    required = {"comms/receipt", "comms/delivery-attempt", "policy/receipt-required"}
    assert required.issubset(registry_tags)
    assert required.issubset(example_tags)

    # Conditional tags are validated only when matching conditions are represented in payloads.


def test_ack_has_required_ack_policy_tags() -> None:
    registry = yaml.safe_load((ROOT / "registries/tag_registry.yaml").read_text())
    registry_tags = {item["canonical_tag"] for item in registry["tags"]}
    example_tags = set(_load_json("examples/comms/acknowledgement.example.json")["tags"])

    required = {"comms/ack", "policy/ack-distinct-from-receipt"}
    assert required.issubset(registry_tags)
    assert required.issubset(example_tags)

    work_outcomes = {"work/completed", "work/blocked", "work/failed"}
    assert len(example_tags & work_outcomes) == 1
    assert (example_tags & work_outcomes).issubset(registry_tags)


def test_notifier_has_required_non_authoritative_tags() -> None:
    registry = yaml.safe_load((ROOT / "registries/tag_registry.yaml").read_text())
    registry_tags = {item["canonical_tag"] for item in registry["tags"]}
    notifier = _load_json("examples/comms/notifier_event.example.json")
    example_tags = set(notifier["tags"])

    required = {
        "comms/notifier",
        "comms/notification-hint",
        "comms/check-authoritative-state",
        "policy/notifier-nonauthoritative",
    }
    assert required.issubset(registry_tags)
    assert required.issubset(example_tags)
    assert notifier["authoritative"] is False

    notifier_paths = {"comms/fs-watch", "comms/session-ping", "comms/polling-fallback"}
    assert len(example_tags & notifier_paths) == 1
    assert (example_tags & notifier_paths).issubset(registry_tags)
