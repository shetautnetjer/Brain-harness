from __future__ import annotations

from plugins.retrieval_router.adapters import (
    lookup_decision_recall,
    lookup_exact_doc,
    lookup_local_canonical_refs,
    lookup_local_memory,
    lookup_plane_b_metadata,
    lookup_task_state,
    resolve_local_sqlite_path,
    sql_narrowing,
)
from plugins.retrieval_router.classifier import classify_query
from src.brain_harness.models import RetrievalResult


def build_query_plan(intent: str) -> list[str]:
    routes = {
        "artifact_lookup": ["exact_doc_or_path_lookup", "local_sqlite_lookup"],
        "local_memory": ["local_sqlite_lookup"],
        "task_state": ["local_tasks_lookup", "local_sqlite_lookup"],
        "decision_recall": ["local_decisions_lookup", "local_sqlite_lookup"],
        "canonical_truth": [
            "local_sqlite_lookup_for_cached_canonical_refs",
            "plane_b_metadata_lookup_if_needed",
        ],
        "fuzzy_exploration": ["sql_narrowing", "vector_fallback"],
    }
    return routes[intent]


def route_query(
    query: str,
    force_plane_b: bool = False,
    agent: str = "main",
    local_db_path: str | None = None,
    plane_b_db_path: str | None = None,
) -> RetrievalResult:
    intent = classify_query(query)
    plan = build_query_plan(intent)
    warnings: list[str] = []
    citations: list[str] = []
    records: list[dict] = []

    resolved_local_db = resolve_local_sqlite_path(agent=agent, explicit_path=local_db_path)

    if intent == "artifact_lookup":
        records, citations, step_warnings = lookup_exact_doc(query, resolved_local_db)
        warnings.extend(step_warnings)
        if not records:
            rows, cites, step_warnings = lookup_local_memory(query, resolved_local_db)
            records.extend(rows)
            citations.extend(cites)
            warnings.extend(step_warnings)

    elif intent == "local_memory":
        records, citations, step_warnings = lookup_local_memory(query, resolved_local_db)
        warnings.extend(step_warnings)

    elif intent == "task_state":
        records, citations, step_warnings = lookup_task_state(query, resolved_local_db)
        warnings.extend(step_warnings)

    elif intent == "decision_recall":
        records, citations, step_warnings = lookup_decision_recall(query, resolved_local_db)
        warnings.extend(step_warnings)

    elif intent == "canonical_truth":
        local_rows, local_citations, step_warnings = lookup_local_canonical_refs(query, resolved_local_db)
        records.extend(local_rows)
        citations.extend(local_citations)
        warnings.extend(step_warnings)

        escalated = force_plane_b or not bool(local_rows)
        if escalated:
            plane_b_rows, plane_b_citations, step_warnings = lookup_plane_b_metadata(query, plane_b_db_path)
            records.extend(plane_b_rows)
            citations.extend(plane_b_citations)
            warnings.extend(step_warnings)
        else:
            warnings.append(
                "plane_b escalation skipped: local canonical references satisfied deterministic canonical lookup"
            )

        return RetrievalResult(
            intent=intent,
            query_plan=plan,
            records=records,
            citations=citations,
            used_vector_search=False,
            escalated_to_plane_b=escalated,
            warnings=warnings,
        )

    elif intent == "fuzzy_exploration":
        rows, cites, step_warnings = sql_narrowing(query, resolved_local_db)
        records.extend(rows)
        citations.extend(cites)
        warnings.extend(step_warnings)
        warnings.append("vector fallback not wired in this patch; deterministic SQL narrowing results returned")

    return RetrievalResult(
        intent=intent,
        query_plan=plan,
        records=records,
        citations=citations,
        used_vector_search=(intent == "fuzzy_exploration"),
        escalated_to_plane_b=False,
        warnings=warnings,
    )
