import sqlite3

from plugins.retrieval_router.router import route_query


def _build_local_db(path: str) -> None:
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE local_docs (doc_id TEXT, text TEXT, content TEXT)")
    conn.execute("CREATE TABLE local_tasks (work_item_id TEXT, title TEXT, status TEXT)")
    conn.execute("CREATE TABLE local_decisions (decision_id TEXT, summary TEXT, text TEXT)")
    conn.execute("CREATE TABLE local_canonical_refs (doc_id TEXT, note TEXT)")

    conn.execute("INSERT INTO local_docs VALUES ('ops-runbook', 'runbook text', 'ops runbook body')")
    conn.execute("INSERT INTO local_tasks VALUES ('wi-2026-03-11-fix', 'Fix retrieval', 'open')")
    conn.execute("INSERT INTO local_decisions VALUES ('dec-1', 'Use deterministic retrieval', 'decision text')")
    conn.execute("INSERT INTO local_canonical_refs VALUES ('policy-source', 'official policy index')")
    conn.commit()
    conn.close()


def _build_plane_b_db(path: str) -> None:
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE canonical_chunks_v2 (chunk_id TEXT, doc_id TEXT, chunk_index INTEGER, text TEXT, "
        "canonical_tags_json TEXT, source_events_json TEXT, indexed_at TEXT)"
    )
    conn.execute(
        "INSERT INTO canonical_chunks_v2 VALUES (?,?,?,?,?,?,?)",
        (
            "canonical-policy::chunk::0",
            "canonical-policy",
            0,
            "official policy text",
            "[]",
            "[]",
            "2026-01-01T00:00:00Z",
        ),
    )
    conn.commit()
    conn.close()


def test_local_memory_routes_to_local_sqlite_first(tmp_path):
    local_db = tmp_path / "main.sqlite"
    _build_local_db(str(local_db))

    out = route_query("runbook", local_db_path=str(local_db))
    assert out.intent == "local_memory"
    assert out.query_plan[0] == "local_sqlite_lookup"
    assert out.records
    assert "local_docs" in out.citations[0]


def test_task_state_routes_to_local_tasks_first(tmp_path):
    local_db = tmp_path / "main.sqlite"
    _build_local_db(str(local_db))

    out = route_query("task retrieval", local_db_path=str(local_db))
    assert out.intent == "task_state"
    assert out.query_plan[0] == "local_tasks_lookup"
    assert out.records
    assert "local_tasks" in out.citations[0]


def test_decision_recall_routes_to_local_decisions_first(tmp_path):
    local_db = tmp_path / "main.sqlite"
    _build_local_db(str(local_db))

    out = route_query("decision retrieval", local_db_path=str(local_db))
    assert out.intent == "decision_recall"
    assert out.query_plan[0] == "local_decisions_lookup"
    assert out.records
    assert "local_decisions" in out.citations[0]


def test_canonical_truth_checks_local_refs_before_plane_b(tmp_path):
    local_db = tmp_path / "main.sqlite"
    plane_b = tmp_path / "canonical.sqlite"
    _build_local_db(str(local_db))
    _build_plane_b_db(str(plane_b))

    out = route_query("canonical policy", local_db_path=str(local_db), plane_b_db_path=str(plane_b))
    assert out.intent == "canonical_truth"
    assert out.query_plan[0] == "local_sqlite_lookup_for_cached_canonical_refs"
    assert out.escalated_to_plane_b is False
    assert any("local canonical references satisfied" in warning for warning in out.warnings)


def test_canonical_truth_escalates_when_local_refs_missing(tmp_path):
    local_db = tmp_path / "main.sqlite"
    plane_b = tmp_path / "canonical.sqlite"
    _build_local_db(str(local_db))
    _build_plane_b_db(str(plane_b))

    conn = sqlite3.connect(local_db)
    conn.execute("DELETE FROM local_canonical_refs")
    conn.commit()
    conn.close()

    out = route_query("canonical policy", local_db_path=str(local_db), plane_b_db_path=str(plane_b))
    assert out.escalated_to_plane_b is True
    assert any("canonical_chunks_v2" in citation for citation in out.citations)


def test_fuzzy_uses_vector_fallback_only_after_sql_narrowing(tmp_path):
    local_db = tmp_path / "main.sqlite"
    _build_local_db(str(local_db))

    out = route_query("need fuzzy runbook hints", local_db_path=str(local_db))
    assert out.intent == "fuzzy_exploration"
    assert out.query_plan[0] == "sql_narrowing"
    assert out.used_vector_search is True
    assert out.records
    assert any("vector fallback not wired" in warning for warning in out.warnings)
