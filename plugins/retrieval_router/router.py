from __future__ import annotations

from plugins.retrieval_router.adapters import local_sqlite_retrieve, plane_b_metadata_retrieve
from plugins.retrieval_router.classifier import classify_query
from src.brain_harness.models import RetrievalResult


def build_query_plan(intent: str) -> list[str]:
    routes = {
        "artifact_lookup": ["exact_doc_or_path_lookup"],
        "local_memory": ["local_sqlite_lookup"],
        "task_state": ["local_tasks_lookup", "local_sqlite_lookup"],
        "decision_recall": ["local_decisions_lookup", "local_sqlite_lookup"],
        # Canonical truth checks local refs first, then conditionally escalates to Plane B metadata.
        "canonical_truth": [
            "local_sqlite_lookup_for_cached_canonical_refs",
            "plane_b_registry_lookup_if_needed",
            "plane_b_metadata_lookup_if_needed",
        ],
        "fuzzy_exploration": ["sql_narrowing", "vector_fallback"],
    }
    return routes[intent]


def route_query(
    query: str,
    force_plane_b: bool = False,
    local_sqlite_paths: list[str] | None = None,
    plane_b_sqlite_paths: list[str] | None = None,
) -> RetrievalResult:
    intent = classify_query(query)
    plan = build_query_plan(intent)
    used_vector = "vector_fallback" in plan

    warnings: list[str] = []
    records: list[dict] = []

    local_intent = "local_memory" if intent == "fuzzy_exploration" else intent
    local_records, local_warnings = local_sqlite_retrieve(query, intent=local_intent, sqlite_paths=local_sqlite_paths)
    warnings.extend(local_warnings)
    records.extend(local_records)

    escalated = False
    if intent == "canonical_truth":
        should_escalate = force_plane_b or not records
        if should_escalate:
            escalated = True
            warnings.append("plane_b registry adapter is still TODO; using metadata adapter directly")
            plane_b_records, plane_b_warnings = plane_b_metadata_retrieve(
                query,
                sqlite_paths=plane_b_sqlite_paths,
            )
            records.extend(plane_b_records)
            warnings.extend(plane_b_warnings)
        else:
            warnings.append(
                "plane_b escalation is conditional and only occurs if local canonical references are insufficient"
            )

    if intent == "fuzzy_exploration":
        warnings.append("vector_fallback is planned but live lancedb wiring remains TODO in this patch")

    return RetrievalResult(
        intent=intent,
        query_plan=plan,
        records=records,
        used_vector_search=used_vector,
        escalated_to_plane_b=escalated,
        warnings=warnings,
    )
