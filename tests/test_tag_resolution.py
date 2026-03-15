import json
from datetime import date


from plugins.tag_guard.validator import validate_tags


def test_alias_resolution_plane_b():
    out = validate_tags([" mem-governance "], "plane_b")
    assert out["resolved_tags"] == ["governance/doctrine"]


def test_alias_resolution_to_canonical_tag_plane_b():
    out = validate_tags(["gate", "policy-lane", "ml-layer"], "plane_b")
    assert out["resolved_tags"] == [
        "governance/promotion-gate",
        "layer/judgment-assistance",
        "retrieval/policy-lane",
    ]


def test_unknown_tag_rejected_on_plane_b_emits_violation(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"
    out = validate_tags(["unknown-tag"], "plane_b", pending_path=str(pending), violation_path=str(violations))
    assert any(("rejected" in e) or ("not allowed" in e) for e in out["errors"])

    rows = [json.loads(line) for line in violations.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["event_type"] == "taxonomy_violation"
    assert rows[0]["severity"] == "error"


def test_pending_family_tag_rejected_on_plane_b(tmp_path):
    violations = tmp_path / "violations.jsonl"
    out = validate_tags(
        ["pending/judgment-model"],
        "plane_b",
        pending_path=str(tmp_path / "pending.jsonl"),
        violation_path=str(violations),
    )
    assert out["resolved_tags"] == []
    assert any(("rejected" in e) or ("not allowed" in e) for e in out["errors"])


def test_unknown_tag_staged_on_plane_a(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"
    out = validate_tags(["new-incoming-tag"], "plane_a", pending_path=str(pending), violation_path=str(violations))
    assert any("staged" in e for e in out["errors"])
    assert pending.exists()
    pending_rows = [json.loads(line) for line in pending.read_text(encoding="utf-8").splitlines()]
    assert pending_rows[0]["tag"] == "new-incoming-tag"


def test_pending_family_tag_allowed_on_plane_a():
    out = validate_tags(["pending/adaptive-learning"], "plane_a")
    assert out["resolved_tags"] == ["pending/adaptive-learning"]
    assert out["errors"] == []


def test_plane_restriction_retrieval_working_lane_rejected_on_plane_b(tmp_path):
    out = validate_tags(
        ["retrieval/working-lane"],
        "plane_b",
        pending_path=str(tmp_path / "pending.jsonl"),
        violation_path=str(tmp_path / "violations.jsonl"),
    )
    assert out["resolved_tags"] == []
    assert any(("rejected" in e) or ("not allowed" in e) for e in out["errors"])


def test_v2_alias_resolution_device_and_identity_plane_b():
    out = validate_tags(["browser", "main-agent"], "plane_b")
    assert out["resolved_tags"] == ["device/web", "identity/main"]


def test_identity_registry_is_limited_to_main_and_arbiter():
    import yaml
    from pathlib import Path

    registry = yaml.safe_load(Path("registries/tag_registry.yaml").read_text(encoding="utf-8"))
    ids = sorted(
        row["canonical_tag"]
        for row in registry.get("tags", [])
        if str(row.get("canonical_tag", "")).startswith("identity/")
    )
    assert ids == ["identity/arbiter", "identity/main"]


def test_memory_canonical_allowed_on_plane_b():
    out = validate_tags(["memory/canonical"], "plane_b")
    assert out["resolved_tags"] == ["memory/canonical"]
    assert out["errors"] == []


def test_canonical_memory_alias_allowed_on_plane_b():
    out = validate_tags(["canonical-memory"], "plane_b")
    assert out["resolved_tags"] == ["memory/canonical"]
    assert out["errors"] == []


def test_memory_canonical_rejected_plane_a_not_staged_pending(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"

    out = validate_tags(
        ["memory/canonical"],
        "plane_a",
        pending_path=str(pending),
        violation_path=str(violations),
    )

    assert out["resolved_tags"] == []
    assert any("not allowed on plane_a" in e for e in out["errors"])
    assert not pending.exists()

    rows = [json.loads(line) for line in violations.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["context"]["action"] == "rejected_plane_disallowed"
    assert rows[0]["context"]["reason"] == "plane_disallowed"


def test_memory_working_rejected_plane_b_not_staged_pending(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"

    out = validate_tags(
        ["memory/working"],
        "plane_b",
        pending_path=str(pending),
        violation_path=str(violations),
    )

    assert out["resolved_tags"] == []
    assert any("not allowed on plane_b" in e for e in out["errors"])
    assert not pending.exists()

    rows = [json.loads(line) for line in violations.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["context"]["action"] == "rejected_plane_disallowed"


def test_unresolved_pending_only_on_plane_a_and_distinct_violation_actions(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"

    out_a = validate_tags(
        ["totally/new-tag"],
        "plane_a",
        pending_path=str(pending),
        violation_path=str(violations),
    )
    out_b = validate_tags(
        ["totally/new-tag"],
        "plane_b",
        pending_path=str(pending),
        violation_path=str(violations),
    )

    assert any("staged" in e for e in out_a["errors"])
    assert any("unknown tag rejected" in e for e in out_b["errors"])

    pending_rows = [json.loads(line) for line in pending.read_text(encoding="utf-8").splitlines()]
    assert len(pending_rows) == 1
    assert pending_rows[0]["action"] == "staged_pending_unknown"
    assert pending_rows[0]["resolution_status"] == "unresolved"

    violation_rows = [json.loads(line) for line in violations.read_text(encoding="utf-8").splitlines()]
    actions = [row["context"]["action"] for row in violation_rows]
    assert actions == ["staged_pending_unknown", "rejected_unknown_plane_b"]

    for row in violation_rows:
        context = row["context"]
        assert context["normalized_tag"] == "totally/new-tag"
        assert context["resolution_status"] == "unresolved"
        assert context["event_id"].startswith("tag_guard_")


def test_canonical_with_empty_plane_list_is_resolved_not_pending(monkeypatch, tmp_path):
    from plugins.tag_guard import validator

    def _fake_registry() -> dict[str, object]:
        return {
            "tags": [
                {
                    "canonical_tag": "memory/no-plane",
                    "planes_allowed": [],
                    "aliases": ["no-plane"],
                }
            ]
        }

    monkeypatch.setattr(validator, "load_registry", _fake_registry)

    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"

    out = validator.validate_tags(
        ["no-plane"],
        "plane_a",
        pending_path=str(pending),
        violation_path=str(violations),
    )

    assert out["resolved_tags"] == []
    assert any("not allowed on plane_a" in e for e in out["errors"])
    assert not pending.exists()

    violation_row = json.loads(violations.read_text(encoding="utf-8").splitlines()[0])
    assert violation_row["context"]["resolution_status"] == "resolved_canonical"
    assert violation_row["context"]["resolved_tag"] == "memory/no-plane"
    assert violation_row["context"]["action"] == "rejected_plane_disallowed"


class _StringableCanonicalMemory:
    def __str__(self) -> str:
        return "memory/canonical"


def test_non_string_raw_tag_serialized_for_unresolved_emission(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"

    out = validate_tags(
        [date(2026, 1, 2)],
        "plane_a",
        pending_path=str(pending),
        violation_path=str(violations),
    )

    assert any("staged" in e for e in out["errors"])

    pending_row = json.loads(pending.read_text(encoding="utf-8").splitlines()[0])
    assert pending_row["raw_tag"] == "2026-01-02"
    assert pending_row["raw_tag_type"] == "date"

    violation_row = json.loads(violations.read_text(encoding="utf-8").splitlines()[0])
    assert violation_row["context"]["raw_tag"] == "2026-01-02"
    assert violation_row["context"]["raw_tag_type"] == "date"


def test_non_string_raw_tag_serialized_for_plane_disallowed_violation(tmp_path):
    violations = tmp_path / "violations.jsonl"

    out = validate_tags(
        [_StringableCanonicalMemory()],
        "plane_a",
        pending_path=str(tmp_path / "pending.jsonl"),
        violation_path=str(violations),
    )

    assert out["resolved_tags"] == []
    assert any("not allowed on plane_a" in e for e in out["errors"])

    violation_row = json.loads(violations.read_text(encoding="utf-8").splitlines()[0])
    assert violation_row["context"]["raw_tag"] == "memory/canonical"
    assert violation_row["context"]["raw_tag_type"] == "_StringableCanonicalMemory"
    assert violation_row["context"]["action"] == "rejected_plane_disallowed"


def test_work_tags_resolve_on_plane_a_and_plane_b():
    out_a = validate_tags(["work/task", "work/completed"], "plane_a")
    out_b = validate_tags(["work/task", "work/completed"], "plane_b")

    assert out_a["resolved_tags"] == ["work/completed", "work/task"]
    assert out_b["resolved_tags"] == ["work/completed", "work/task"]
    assert out_a["errors"] == []
    assert out_b["errors"] == []


def test_project_tags_resolve_on_plane_a_and_plane_b():
    out_a = validate_tags(["projects/config-safety", "projects/trading-brain"], "plane_a")
    out_b = validate_tags(["projects/config-safety", "projects/trading-brain"], "plane_b")

    assert out_a["resolved_tags"] == ["projects/config-safety", "projects/trading-brain"]
    assert out_b["resolved_tags"] == ["projects/config-safety", "projects/trading-brain"]
    assert out_a["errors"] == []
    assert out_b["errors"] == []


def test_comms_tags_admit_correctly_across_planes(tmp_path):
    out_both_a = validate_tags(["comms/mailbox", "comms/agent-route"], "plane_a")
    out_both_b = validate_tags(["comms/mailbox", "comms/agent-route"], "plane_b")

    assert out_both_a["resolved_tags"] == ["comms/agent-route", "comms/mailbox"]
    assert out_both_b["resolved_tags"] == ["comms/agent-route", "comms/mailbox"]

    out_plane_a_only = validate_tags(
        ["comms/notifier"],
        "plane_b",
        pending_path=str(tmp_path / "pending.jsonl"),
        violation_path=str(tmp_path / "violations.jsonl"),
    )
    assert out_plane_a_only["resolved_tags"] == []
    assert any("not allowed on plane_b" in e for e in out_plane_a_only["errors"])


def test_pending_lobster_tags_stay_pending():
    import yaml
    from pathlib import Path

    main = yaml.safe_load(Path("registries/tag_registry.yaml").read_text(encoding="utf-8"))
    comms = yaml.safe_load(Path("registries/tag_registry.comms.yaml").read_text(encoding="utf-8"))

    main_tags = {row["canonical_tag"]: row for row in main.get("tags", [])}
    comms_tags = {row["canonical_tag"]: row for row in comms.get("tags", [])}

    assert main_tags["workflow-substrate/lobster"]["status"] == "pending"
    assert comms_tags["workflow-substrate/lobster"]["status"] == "pending"
    assert comms_tags["comms/lobster-adapter"]["status"] == "pending"
