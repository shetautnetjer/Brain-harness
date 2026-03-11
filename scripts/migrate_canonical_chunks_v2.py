from __future__ import annotations

"""Starter migration for canonical_chunks_v2.

Legacy `canonical_chunks` is read-only input.
TODO: wire real SQL transactions and backfill logic in production runtime.
"""

from plugins.tag_guard.normalize import normalize_doc_id

CANONICAL_CHUNKS_V2_DDL = """
CREATE TABLE IF NOT EXISTS canonical_chunks_v2 (
  chunk_id TEXT PRIMARY KEY,
  doc_id TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  text TEXT NOT NULL,
  canonical_tags_json TEXT NOT NULL DEFAULT '[]',
  aliases_json TEXT NOT NULL DEFAULT '[]',
  source_events_json TEXT NOT NULL DEFAULT '[]',
  source_plane TEXT NOT NULL,
  ingest_run_id TEXT NOT NULL,
  promotion_packet_id TEXT,
  embedding_model TEXT NOT NULL,
  embedding_dim INTEGER NOT NULL,
  indexed_at TEXT NOT NULL
);
""".strip()


def transform_row(row: dict) -> dict:
    doc_id = normalize_doc_id(row["doc_id"])
    chunk_index = int(row["chunk_index"])
    return {
        "chunk_id": f"{doc_id}::chunk::{chunk_index}",
        "doc_id": doc_id,
        "chunk_index": chunk_index,
        "text": row["text"],
        "canonical_tags_json": row.get("canonical_tags_json", row.get("tags_json", "[]")),
        "aliases_json": row.get("aliases_json", "[]"),
        "source_events_json": row.get("source_events_json", "[]"),
        "source_plane": row.get("source_plane", "plane_b"),
        "ingest_run_id": row.get("ingest_run_id"),
        "promotion_packet_id": row.get("promotion_packet_id"),
        "embedding_model": row.get("embedding_model"),
        "embedding_dim": row.get("embedding_dim"),
        "indexed_at": row.get("indexed_at"),
    }


def main() -> None:
    print("legacy table: canonical_chunks (read-only)")
    print("target table: canonical_chunks_v2")
    print("DDL preview:\n" + CANONICAL_CHUNKS_V2_DDL)
    print("TODO: connect to SQLite and run SELECT/INSERT with provenance validation")


if __name__ == "__main__":
    main()
