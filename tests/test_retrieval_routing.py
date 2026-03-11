from plugins.retrieval_router.router import route_query


def test_fuzzy_uses_vector_fallback_not_first_step():
    out = route_query("need fuzzy memory hints")
    assert out.intent == "fuzzy_exploration"
    assert out.query_plan[0] == "sql_narrowing"
    assert out.used_vector_search is True
