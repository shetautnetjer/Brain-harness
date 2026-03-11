from __future__ import annotations

import argparse

from plugins.tag_guard.normalize import normalize_chunk_id, normalize_doc_id


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("doc_id")
    parser.add_argument("chunk_index", type=int)
    args = parser.parse_args()
    print("normalized_doc_id:", normalize_doc_id(args.doc_id))
    print("normalized_chunk_id:", normalize_chunk_id(args.doc_id, args.chunk_index))


if __name__ == "__main__":
    main()
