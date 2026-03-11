"""Deterministic SQLite retrieval adapters.

These adapters intentionally focus on deterministic SQL lookup against known/local SQLite files.
Vector retrieval remains a TODO fallback path.
"""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any


def _load_inventory(path: str = "manifests/runtime/inventory_snapshot.example.json") -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def resolve_local_sqlite_path(agent: str, explicit_path: str | None = None) -> str | None:
    if explicit_path:
        return explicit_path
    inv = _load_inventory()
    for path in inv.get("sqlite_paths", []):
        if path.endswith(f"/{agent}.sqlite"):
            return path
    return None


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
    return row is not None


def _fetch_rows(conn: sqlite3.Connection, sql: str, args: tuple[Any, ...]) -> list[dict[str, Any]]:
    cursor = conn.execute(sql, args)
    cols = [item[0] for item in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row[1] for row in rows}


def _like_query_for_columns(table: str, columns: set[str], preferred: tuple[str, ...]) -> str | None:
    active = [col for col in preferred if col in columns]
    if not active:
        return None
    clause = " OR ".join([f"lower({col}) LIKE ?" for col in active])
    return f"SELECT * FROM {table} WHERE {clause} LIMIT 25"




def _search_tokens(query: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9\-]+", query.lower())
    tokens = [t for t in tokens if len(t) > 2]
    return tokens or [query.lower()]


def _run_like_search(conn: sqlite3.Connection, table: str, columns: set[str], preferred: tuple[str, ...], query: str) -> list[dict[str, Any]]:
    sql = _like_query_for_columns(table, columns, preferred)
    if not sql:
        return []
    placeholders = sql.count("?")
    for token in _search_tokens(query):
        rows = _fetch_rows(conn, sql, tuple([f"%{token}%"] * placeholders))
        if rows:
            return rows
    return []

def _open_db(path: str | None) -> tuple[sqlite3.Connection | None, list[str]]:
    if not path:
        return None, ["no sqlite path configured for adapter"]
    p = Path(path)
    if not p.exists():
        return None, [f"sqlite path not found: {path}"]
    return sqlite3.connect(path), []


def extract_doc_id_hint(query: str) -> str | None:
    match = re.search(r"doc_id:([a-z0-9\-]+)", query.lower())
    if match:
        return match.group(1)
    return None


def lookup_exact_doc(query: str, local_db_path: str | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    doc_id = extract_doc_id_hint(query)
    if not doc_id:
        return [], [], ["exact lookup skipped: no doc_id:<value> hint"]

    conn, warnings = _open_db(local_db_path)
    if not conn:
        return [], [], warnings

    try:
        for table in ("local_docs", "docs", "documents"):
            if not _table_exists(conn, table):
                continue
            rows = _fetch_rows(
                conn,
                f"SELECT doc_id, * FROM {table} WHERE doc_id = ? LIMIT 10",
                (doc_id,),
            )
            if rows:
                return rows, [f"sqlite:{local_db_path}:{table}:doc_id={doc_id}"], warnings
        warnings.append("exact lookup found no compatible doc table")
        return [], [], warnings
    finally:
        conn.close()


def lookup_local_memory(query: str, local_db_path: str | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    conn, warnings = _open_db(local_db_path)
    if not conn:
        return [], [], warnings
    try:
        for table in ("local_docs", "docs", "documents"):
            if not _table_exists(conn, table):
                continue
            columns = _table_columns(conn, table)
            rows = _run_like_search(conn, table, columns, ("doc_id", "text", "content", "body", "title"), query)
            return rows, [f"sqlite:{local_db_path}:{table}:like"], warnings
        warnings.append("local memory lookup found no compatible doc table")
        return [], [], warnings
    finally:
        conn.close()


def lookup_task_state(query: str, local_db_path: str | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    conn, warnings = _open_db(local_db_path)
    if not conn:
        return [], [], warnings
    try:
        if _table_exists(conn, "local_tasks"):
            columns = _table_columns(conn, "local_tasks")
            rows = _run_like_search(conn, "local_tasks", columns, ("work_item_id", "title", "status", "text"), query)
            return rows, [f"sqlite:{local_db_path}:local_tasks:like"], warnings
        warnings.append("task lookup fallback to local memory table")
        rows, cites, extra = lookup_local_memory(query, local_db_path)
        return rows, cites, warnings + extra
    finally:
        conn.close()


def lookup_decision_recall(query: str, local_db_path: str | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    conn, warnings = _open_db(local_db_path)
    if not conn:
        return [], [], warnings
    try:
        for table in ("local_decisions", "decisions"):
            if _table_exists(conn, table):
                columns = _table_columns(conn, table)
                rows = _run_like_search(conn, table, columns, ("decision_id", "summary", "text", "doc_id"), query)
                return rows, [f"sqlite:{local_db_path}:{table}:like"], warnings
        warnings.append("decision lookup fallback to local memory table")
        rows, cites, extra = lookup_local_memory(query, local_db_path)
        return rows, cites, warnings + extra
    finally:
        conn.close()


def lookup_local_canonical_refs(query: str, local_db_path: str | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    conn, warnings = _open_db(local_db_path)
    if not conn:
        return [], [], warnings
    try:
        for table in ("local_canonical_refs", "canonical_refs"):
            if _table_exists(conn, table):
                columns = _table_columns(conn, table)
                rows = _run_like_search(conn, table, columns, ("doc_id", "note", "text"), query)
                return rows, [f"sqlite:{local_db_path}:{table}:like"], warnings
        warnings.append("no local canonical reference table found")
        return [], [], warnings
    finally:
        conn.close()


def lookup_plane_b_metadata(query: str, plane_b_db_path: str | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    conn, warnings = _open_db(plane_b_db_path)
    if not conn:
        return [], [], warnings
    try:
        if not _table_exists(conn, "canonical_chunks_v2"):
            return [], [], warnings + ["canonical_chunks_v2 table not found in plane_b store"]
        columns = _table_columns(conn, "canonical_chunks_v2")
        search_cols = [col for col in ("doc_id", "text") if col in columns]
        if not search_cols:
            return [], [], warnings + ["canonical_chunks_v2 missing searchable columns doc_id/text"]
        where = " OR ".join([f"lower({col}) LIKE ?" for col in search_cols])
        sql = (
            "SELECT chunk_id, doc_id, chunk_index, canonical_tags_json, source_events_json, indexed_at "
            f"FROM canonical_chunks_v2 WHERE {where} LIMIT 25"
        )
        for token in _search_tokens(query):
            rows = _fetch_rows(conn, sql, tuple([f"%{token}%"] * len(search_cols)))
            if rows:
                return rows, [f"sqlite:{plane_b_db_path}:canonical_chunks_v2:like"], warnings
        return [], [f"sqlite:{plane_b_db_path}:canonical_chunks_v2:like"], warnings
    finally:
        conn.close()


def sql_narrowing(query: str, local_db_path: str | None) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    return lookup_local_memory(query=query, local_db_path=local_db_path)
