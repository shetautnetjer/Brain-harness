from plugins.qmd_guard.validator import validate_frontmatter


def test_plane_b_source_events_required_for_promoted_observation():
    rules = {"doc_type_rules": {"promoted_observation": {"require_source_events_on_plane_b": True}}}
    fm = {"doc_id": "x", "doc_type": "promoted_observation", "tags": ["promotion"]}
    errors = validate_frontmatter(fm, "plane_b", rules)
    assert any("source_events required" in e for e in errors)


def test_plane_b_explicit_exemption_from_doc_type_rules():
    rules = {"doc_type_rules": {"schema_artifact": {"require_source_events_on_plane_b": False}}}
    fm = {"doc_id": "root schema", "doc_type": "schema_artifact", "tags": ["memory-governance"]}
    errors = validate_frontmatter(fm, "plane_b", rules)
    assert not any("source_events required" in e for e in errors)


def test_doc_id_normalized_and_tags_only_from_frontmatter():
    rules = {"doc_type_rules": {"note": {"require_source_events_on_plane_b": False}}}
    fm = {
        "doc_id": "My_Doc__Name",
        "doc_type": "note",
        "tags": ["memory-governance"],
        "source_path": "/tmp/folder/secret-tag/another-tag.qmd",
    }
    errors = validate_frontmatter(fm, "plane_a", rules)
    assert errors == []
    assert fm["doc_id"] == "my-doc-name"
    assert fm["tags"] == ["memory-governance"]
