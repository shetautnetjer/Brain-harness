from __future__ import annotations

"""Starter migration for canonical_chunks_v2.

Legacy `canonical_chunks` is treated as read-only input.
TODO: wire actual SQL connection and transaction handling.
"""

from plugins.tag_guard.normalize import normalize_doc_id


def transform_row(row: dict) -> dict:
    return {
        "chunk_id": f"{normalize_doc_id(row['doc_id'])}::chunk::{row['chunk_index']}",
        "doc_id": normalize_doc_id(row["doc_id"]),
        "chunk_index": row["chunk_index"],
        "text": row["text"],
        "source_events_json": row.get("source_events_json", "[]"),
        "tags_json": row.get("tags_json", "[]"),
        "embedding_model": row.get("embedding_model"),
        "embedding_dim": row.get("embedding_dim"),
        "source_plane": "plane_b",
        "ingest_run_id": row.get("ingest_run_id"),
        "indexed_at": row.get("indexed_at"),
    }


def main() -> None:
    print("TODO: perform SELECT from legacy canonical_chunks and INSERT into canonical_chunks_v2")


if __name__ == "__main__":
    main()
