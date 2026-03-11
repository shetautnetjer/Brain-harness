import sqlite3

from plugins.retrieval_router.router import route_query


def _db(path, ddl, rows):
    conn = sqlite3.connect(path)
    try:
        conn.execute(ddl)
        if rows:
            placeholders = ",".join(["?"] * len(rows[0]))
            table = ddl.split("(")[0].split()[-1]
            conn.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
        conn.commit()
    finally:
        conn.close()


def test_local_memory_routes_to_local_sqlite_first(tmp_path):
    local_db = tmp_path / "local.sqlite"
    _db(
        str(local_db),
        "CREATE TABLE memory (id TEXT, text TEXT)",
        [("m1", "hello local memory")],
    )

    out = route_query("hello", local_sqlite_paths=[str(local_db)])
    assert out.intent == "local_memory"
    assert out.query_plan[0] == "local_sqlite_lookup"
    assert out.records
    assert out.records[0]["_adapter"] == "local_sqlite"
    assert out.records[0]["_source_table"] == "memory"


def test_task_state_routes_to_task_tables_first(tmp_path):
    local_db = tmp_path / "tasks.sqlite"
    _db(
        str(local_db),
        "CREATE TABLE tasks (id TEXT, text TEXT)",
        [("t1", "task status green")],
    )

    out = route_query("task status", local_sqlite_paths=[str(local_db)])
    assert out.intent == "task_state"
    assert out.query_plan[0] == "local_tasks_lookup"
    assert out.records
    assert out.records[0]["_source_table"] == "tasks"


def test_decision_recall_routes_to_decision_tables_first(tmp_path):
    local_db = tmp_path / "decisions.sqlite"
    _db(
        str(local_db),
        "CREATE TABLE decisions (id TEXT, text TEXT)",
        [("d1", "decision memo")],
    )

    out = route_query("decision memo", local_sqlite_paths=[str(local_db)])
    assert out.intent == "decision_recall"
    assert out.query_plan[0] == "local_decisions_lookup"
    assert out.records
    assert out.records[0]["_source_table"] == "decisions"


def test_canonical_truth_checks_local_refs_then_conditionally_plane_b(tmp_path):
    local_db = tmp_path / "local.sqlite"
    plane_b_db = tmp_path / "plane_b.sqlite"
    _db(
        str(local_db),
        "CREATE TABLE canonical_refs (doc_id TEXT, text TEXT)",
        [("canonical policy-1", "local canonical pointer")],
    )
    _db(
        str(plane_b_db),
        "CREATE TABLE canonical_chunks_v2 (chunk_id TEXT, doc_id TEXT, chunk_index INTEGER, text TEXT, canonical_tags_json TEXT, source_plane TEXT, indexed_at TEXT)",
        [("policy-1::chunk::0", "canonical policy-1", 0, "plane b canonical text", "[]", "plane_b", "2026-01-01")],
    )

    out_local_only = route_query(
        "canonical policy-1",
        local_sqlite_paths=[str(local_db)],
        plane_b_sqlite_paths=[str(plane_b_db)],
    )
    assert out_local_only.intent == "canonical_truth"
    assert out_local_only.query_plan[0] == "local_sqlite_lookup_for_cached_canonical_refs"
    assert out_local_only.escalated_to_plane_b is False
    assert out_local_only.records[0]["_source_table"] == "canonical_refs"

    out_escalated = route_query(
        "canonical policy-1",
        force_plane_b=True,
        local_sqlite_paths=[str(local_db)],
        plane_b_sqlite_paths=[str(plane_b_db)],
    )
    assert out_escalated.escalated_to_plane_b is True
    assert any(r["_adapter"] == "plane_b_metadata" for r in out_escalated.records)


def test_fuzzy_exploration_uses_vector_fallback_only_after_sql_narrowing(tmp_path):
    local_db = tmp_path / "local.sqlite"
    _db(
        str(local_db),
        "CREATE TABLE document_chunks (chunk_id TEXT, text TEXT)",
        [("c1", "fuzzy memory hints live here")],
    )

    out = route_query("fuzzy memory hints", local_sqlite_paths=[str(local_db)])
    assert out.intent == "fuzzy_exploration"
    assert out.query_plan[0] == "sql_narrowing"
    assert out.used_vector_search is True
    assert out.records
    assert out.records[0]["_source_table"] == "document_chunks"
    assert any("lancedb wiring remains TODO" in w for w in out.warnings)
