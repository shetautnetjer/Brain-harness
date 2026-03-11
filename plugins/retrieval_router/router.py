from __future__ import annotations

from plugins.retrieval_router.classifier import classify_query
from src.brain_harness.models import RetrievalResult


def build_query_plan(intent: str) -> list[str]:
    routes = {
        "artifact_lookup": ["exact_doc_or_path_lookup"],
        "local_memory": ["local_sqlite_lookup"],
        "task_state": ["local_tasks_lookup", "local_sqlite_lookup"],
        "decision_recall": ["local_decisions_lookup", "local_sqlite_lookup"],
        "canonical_truth": ["plane_b_registry_lookup", "plane_b_metadata_lookup"],
        "fuzzy_exploration": ["sql_narrowing", "vector_fallback"],
    }
    return routes[intent]


def route_query(query: str) -> RetrievalResult:
    intent = classify_query(query)
    plan = build_query_plan(intent)
    return RetrievalResult(
        intent=intent,
        query_plan=plan,
        used_vector_search=("vector_fallback" in plan),
        escalated_to_plane_b=(intent == "canonical_truth"),
    )
