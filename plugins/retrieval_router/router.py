from __future__ import annotations

from plugins.retrieval_router.classifier import classify_query
from src.brain_harness.models import RetrievalResult


def build_query_plan(intent: str) -> list[str]:
    routes = {
        "artifact_lookup": ["exact_doc_or_path_lookup"],
        "local_memory": ["local_sqlite_lookup"],
        "task_state": ["local_tasks_lookup", "local_sqlite_lookup"],
        "decision_recall": ["local_decisions_lookup", "local_sqlite_lookup"],
        # Canonical truth checks local cache/index pointers first, then escalates if unresolved.
        "canonical_truth": [
            "local_sqlite_lookup_for_cached_canonical_refs",
            "plane_b_registry_lookup_if_needed",
            "plane_b_metadata_lookup_if_needed",
        ],
        "fuzzy_exploration": ["sql_narrowing", "vector_fallback"],
    }
    return routes[intent]


def route_query(query: str, force_plane_b: bool = False) -> RetrievalResult:
    intent = classify_query(query)
    plan = build_query_plan(intent)
    used_vector = "vector_fallback" in plan

    escalated = force_plane_b and intent == "canonical_truth"
    warnings: list[str] = []
    if intent == "canonical_truth" and not force_plane_b:
        warnings.append("plane_b escalation is conditional and only occurs if local canonical references are insufficient")

    return RetrievalResult(
        intent=intent,
        query_plan=plan,
        used_vector_search=used_vector,
        escalated_to_plane_b=escalated,
        warnings=warnings,
    )
