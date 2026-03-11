from __future__ import annotations

"""Deterministic retrieval adapters for local SQLite + Plane B metadata.

These adapters are intentionally conservative:
- deterministic SQL lookups first
- Plane B metadata only for canonical escalation
- vector retrieval remains explicit TODO
"""

import glob
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

import yaml

DEFAULT_SYSTEM_MANIFEST_PATH = "manifests/runtime/system_manifest.example.yaml"
DEFAULT_RUNTIME_SNAPSHOT_PATH = "manifests/runtime/inventory_snapshot.example.json"


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
    return row is not None


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}


def _discover_local_sqlite_paths(
    system_manifest_path: str = DEFAULT_SYSTEM_MANIFEST_PATH,
    runtime_snapshot_path: str = DEFAULT_RUNTIME_SNAPSHOT_PATH,
) -> list[str]:
    env_paths = os.environ.get("BRAIN_HARNESS_LOCAL_SQLITE_PATHS")
    if env_paths:
        return [p.strip() for p in env_paths.split(":") if p.strip()]

    found: list[str] = []

    manifest = Path(system_manifest_path)
    if manifest.exists():
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        glob_pattern = ((data.get("openclaw") or {}).get("known_sqlite_glob"))
        if isinstance(glob_pattern, str):
            found.extend(sorted(glob.glob(glob_pattern)))

    snapshot = Path(runtime_snapshot_path)
    if snapshot.exists():
        data = json.loads(snapshot.read_text(encoding="utf-8"))
        for key in ("discovered_sqlite_paths", "sqlite_paths"):
            for path in data.get(key, []):
                if isinstance(path, str):
                    found.append(path)

    unique_existing: list[str] = []
    seen: set[str] = set()
    for p in found:
        if p not in seen and Path(p).exists():
            seen.add(p)
            unique_existing.append(p)
    return unique_existing


def _local_table_preferences(intent: str) -> list[str]:
    by_intent = {
        "task_state": ["tasks", "task_state", "task_states", "todo_tasks", "document_chunks"],
        "decision_recall": ["decisions", "decision_log", "decision_records", "document_chunks"],
        "canonical_truth": ["canonical_refs", "canonical_references", "document_aliases", "document_chunks"],
        "local_memory": ["memory", "notes", "document_chunks", "documents"],
        "artifact_lookup": ["document_aliases", "document_chunks", "documents"],
        "fuzzy_exploration": ["document_chunks", "memory", "notes"],
    }
    return by_intent.get(intent, ["document_chunks", "documents", "memory"])


def _query_table(conn: sqlite3.Connection, table: str, query: str, limit: int = 5) -> list[dict[str, Any]]:
    cols = _table_columns(conn, table)
    if not cols:
        return []

    target_col = next((c for c in ("doc_id", "document_id", "path", "chunk_id", "id") if c in cols), None)
    text_col = next((c for c in ("text", "content", "body", "value", "title") if c in cols), None)
    if not target_col and not text_col:
        return []

    if target_col:
        sql = f"SELECT * FROM {table} WHERE {target_col} = ? LIMIT ?"
        rows = conn.execute(sql, (query, limit)).fetchall()
        if rows:
            names = [d[0] for d in conn.execute(f"SELECT * FROM {table} LIMIT 0").description or []]
            return [dict(zip(names, row)) for row in rows]

    if text_col:
        sql = f"SELECT * FROM {table} WHERE {text_col} LIKE ? LIMIT ?"
        rows = conn.execute(sql, (f"%{query}%", limit)).fetchall()
        names = [d[0] for d in conn.execute(f"SELECT * FROM {table} LIMIT 0").description or []]
        return [dict(zip(names, row)) for row in rows]

    return []


def local_sqlite_retrieve(
    query: str,
    intent: str,
    sqlite_paths: list[str] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    paths = sqlite_paths if sqlite_paths is not None else _discover_local_sqlite_paths()
    if not paths:
        return [], ["no local sqlite paths discovered for deterministic retrieval"]

    warnings: list[str] = []
    results: list[dict[str, Any]] = []
    for db_path in paths:
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
        except sqlite3.Error as exc:
            warnings.append(f"failed to open sqlite path {db_path}: {exc}")
            continue

        try:
            for table in _local_table_preferences(intent):
                if not _table_exists(conn, table):
                    continue
                for row in _query_table(conn, table, query):
                    payload = dict(row)
                    payload["_adapter"] = "local_sqlite"
                    payload["_source_db"] = db_path
                    payload["_source_table"] = table
                    results.append(payload)
                if results:
                    break
        finally:
            conn.close()

        if results:
            break

    return results, warnings


def plane_b_metadata_retrieve(
    query: str,
    sqlite_paths: list[str] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    paths = sqlite_paths
    if paths is None:
        env_paths = os.environ.get("BRAIN_HARNESS_PLANE_B_SQLITE_PATHS")
        paths = [p.strip() for p in env_paths.split(":") if p.strip()] if env_paths else []

    if not paths:
        return [], ["plane_b metadata lookup skipped: no configured plane_b sqlite paths"]

    warnings: list[str] = []
    results: list[dict[str, Any]] = []
    for db_path in paths:
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
        except sqlite3.Error as exc:
            warnings.append(f"failed to open plane_b sqlite path {db_path}: {exc}")
            continue

        try:
            if not _table_exists(conn, "canonical_chunks_v2"):
                continue
            cols = _table_columns(conn, "canonical_chunks_v2")
            if not {"doc_id", "text"}.issubset(cols):
                warnings.append(f"canonical_chunks_v2 missing expected columns in {db_path}")
                continue

            rows = conn.execute(
                """
                SELECT chunk_id, doc_id, chunk_index, text, canonical_tags_json, source_plane, indexed_at
                FROM canonical_chunks_v2
                WHERE doc_id = ? OR text LIKE ?
                ORDER BY chunk_index ASC
                LIMIT 5
                """,
                (query, f"%{query}%"),
            ).fetchall()
            for row in rows:
                payload = dict(row)
                payload["_adapter"] = "plane_b_metadata"
                payload["_source_db"] = db_path
                payload["_source_table"] = "canonical_chunks_v2"
                results.append(payload)
            if results:
                break
        finally:
            conn.close()

    return results, warnings
