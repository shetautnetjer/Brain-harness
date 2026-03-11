from __future__ import annotations

INTENTS = {
    "artifact": "artifact_lookup",
    "file": "artifact_lookup",
    "task": "task_state",
    "decision": "decision_recall",
    "official": "canonical_truth",
    "canonical": "canonical_truth",
    "fuzzy": "fuzzy_exploration",
}


def classify_query(query: str) -> str:
    q = query.lower()
    for token, intent in INTENTS.items():
        if token in q:
            return intent
    return "local_memory"
