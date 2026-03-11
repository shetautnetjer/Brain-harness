from plugins.provenance_guard.validator import validate_vector_write


def test_required_provenance_fields():
    errors = validate_vector_write({"embedding_model": "e5"})
    assert "missing required provenance field: embedding_dim" in errors
