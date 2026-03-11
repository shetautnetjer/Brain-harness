from plugins.provenance_guard.validator import (
    validate_batch_plane_consistency,
    validate_plane_separation,
    validate_vector_write,
)


def test_required_provenance_fields():
    errors = validate_vector_write({"embedding_model": "e5"})
    assert "missing required provenance field: embedding_dim" in errors


def test_invalid_provenance_shape_rejected():
    errors = validate_vector_write(
        {
            "embedding_model": "e5",
            "embedding_dim": 0,
            "source_plane": "bad_plane",
            "ingest_run_id": "run_1",
            "indexed_at": "not-a-ts",
        }
    )
    assert "embedding_dim must be a positive integer" in errors
    assert "source_plane must be one of: plane_a, plane_b" in errors
    assert "indexed_at must be an ISO-8601 timestamp" in errors


def test_plane_mixing_failure():
    err = validate_plane_separation("plane_a", "plane_b")
    assert any("plane separation violation" in row for row in err)


def test_batch_plane_mixing_failure():
    err = validate_batch_plane_consistency([
        {"source_plane": "plane_a"},
        {"source_plane": "plane_b"},
    ])
    assert any("mixed source_plane values" in row for row in err)
