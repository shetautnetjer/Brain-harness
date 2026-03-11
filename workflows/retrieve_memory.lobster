workflow retrieve_memory {
  step classify_query using llm-task(prompt="prompts/codex/json_classifier_prompt.md")
  step deterministic_lookup using retrieval_router
  step vector_fallback when intent == "fuzzy_exploration"
  step emit_audit_jsonl
}
