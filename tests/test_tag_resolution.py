import json
from pathlib import Path

from plugins.tag_guard.validator import validate_tags


def test_alias_resolution_plane_b():
    out = validate_tags([" mem-governance "], "plane_b")
    assert out["resolved_tags"] == ["memory-governance"]


def test_unknown_tag_rejected_on_plane_b_emits_violation(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"
    out = validate_tags(["unknown-tag"], "plane_b", pending_path=str(pending), violation_path=str(violations))
    assert any("rejected" in e for e in out["errors"])

    rows = [json.loads(line) for line in violations.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["event_type"] == "taxonomy_violation"
    assert rows[0]["severity"] == "error"


def test_unknown_tag_staged_on_plane_a(tmp_path):
    pending = tmp_path / "pending.jsonl"
    violations = tmp_path / "violations.jsonl"
    out = validate_tags(["new-incoming-tag"], "plane_a", pending_path=str(pending), violation_path=str(violations))
    assert any("staged" in e for e in out["errors"])
    assert pending.exists()
    pending_rows = [json.loads(line) for line in pending.read_text(encoding="utf-8").splitlines()]
    assert pending_rows[0]["tag"] == "new-incoming-tag"
