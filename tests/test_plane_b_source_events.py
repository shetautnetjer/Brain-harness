from plugins.qmd_guard.validator import validate_frontmatter


def test_plane_b_source_events_required_for_promoted_observation():
    rules = {"doc_type_rules": {"promoted_observation": {"require_source_events_on_plane_b": True}}}
    fm = {"doc_id": "x", "doc_type": "promoted_observation", "tags": ["promotion"]}
    errors = validate_frontmatter(fm, "plane_b", rules)
    assert any("source_events required" in e for e in errors)
