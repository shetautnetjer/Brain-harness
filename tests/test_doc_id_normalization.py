from plugins.tag_guard.normalize import normalize_chunk_id, normalize_doc_id


def test_doc_id_normalization():
    assert normalize_doc_id("  My_Doc__Name  ") == "my-doc-name"


def test_chunk_id_normalization():
    assert normalize_chunk_id("My_Doc", 3) == "my-doc::chunk::3"
