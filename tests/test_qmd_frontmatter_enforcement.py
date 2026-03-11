from plugins.qmd_guard.validator import validate_frontmatter


def test_tags_validation_runs_even_when_tags_shape_is_invalid():
    rules = {"doc_type_rules": {"note": {"require_source_events_on_plane_b": True}}}
    fm = {"doc_id": "x", "doc_type": "note", "tags": "not-a-list"}
    errors = validate_frontmatter(fm, "plane_b", rules)

    assert "tags must be a list in frontmatter" in errors
    # If validation short-circuits, this plane_b enforcement would never run.
    assert any("source_events required" in e for e in errors)


def test_plane_b_global_required_fields_are_enforced():
    rules = {
        "global_required_frontmatter_by_plane": {
            "plane_b": [
                "doc_id",
                "doc_type",
                "trust_zone",
                "status",
                "created_at",
                "updated_at",
                "tags",
                "canonical",
            ]
        },
        "doc_type_rules": {"schema_artifact": {"require_source_events_on_plane_b": False}},
    }
    fm = {"doc_id": "x", "doc_type": "schema_artifact", "tags": []}
    errors = validate_frontmatter(fm, "plane_b", rules)

    assert "missing required field: trust_zone" in errors
    assert "missing required field: status" in errors
    assert "missing required field: created_at" in errors
    assert "missing required field: updated_at" in errors
    assert "missing required field: canonical" in errors


def test_doc_type_specific_required_frontmatter_is_config_driven():
    rules = {
        "doc_type_rules": {
            "policy_doc": {
                "require_source_events_on_plane_b": True,
                "required_frontmatter": ["summary"],
            }
        }
    }
    fm = {
        "doc_id": "policy-doc",
        "doc_type": "policy_doc",
        "tags": ["memory-governance"],
        "source_events": ["evt_123"],
    }
    errors = validate_frontmatter(fm, "plane_b", rules)
    assert "missing required field for doc_type 'policy_doc': summary" in errors


def test_recommended_list_fields_warn_on_wrong_shape_without_over_rejecting():
    rules = {"doc_type_rules": {"schema_artifact": {"require_source_events_on_plane_b": False}}}
    fm = {
        "doc_id": "schema",
        "doc_type": "schema_artifact",
        "tags": ["memory-governance"],
        "source_events": "evt_123",
    }
    errors = validate_frontmatter(fm, "plane_a", rules)
    assert "source_events should be a list when provided" in errors
