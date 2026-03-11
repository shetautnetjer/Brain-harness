from plugins.tag_guard.validator import validate_tags


def test_alias_resolution_plane_b():
    out = validate_tags(["mem-governance"], "plane_b")
    assert out["resolved_tags"] == ["memory-governance"]


def test_unknown_tag_rejected_on_plane_b():
    out = validate_tags(["unknown-tag"], "plane_b")
    assert any("rejected" in e for e in out["errors"])
