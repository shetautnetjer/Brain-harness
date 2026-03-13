import json

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
    assert any("rejected" in e for e in out["errors"])

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
    assert any("rejected" in e for e in out["errors"])


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
    assert any("rejected" in e for e in out["errors"])


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
