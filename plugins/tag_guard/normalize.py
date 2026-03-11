from __future__ import annotations

import re


def normalize_doc_id(raw: str) -> str:
    value = raw.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9\-\s]", "", value)
    value = re.sub(r"[\s\-]+", "-", value)
    return value.strip("-")


def normalize_chunk_id(doc_id: str, chunk_index: int) -> str:
    return f"{normalize_doc_id(doc_id)}::chunk::{chunk_index}"
