from plugins.retrieval_router.router import route_query


def test_fuzzy_uses_vector_fallback_not_first_step():
    out = route_query("need fuzzy memory hints")
    assert out.intent == "fuzzy_exploration"
    assert out.query_plan[0] == "sql_narrowing"
    assert out.used_vector_search is True


def test_canonical_truth_is_conditional_escalation_by_default():
    out = route_query("what is the canonical policy for promotions")
    assert out.intent == "canonical_truth"
    assert out.query_plan[0] == "local_sqlite_lookup_for_cached_canonical_refs"
    assert out.escalated_to_plane_b is False
    assert out.warnings


def test_canonical_truth_can_force_plane_b_escalation():
    out = route_query("official ruling", force_plane_b=True)
    assert out.intent == "canonical_truth"
    assert out.escalated_to_plane_b is True
