from __future__ import annotations


def route_plane(needs_canonical: bool) -> str:
    return "plane_b" if needs_canonical else "plane_a"
