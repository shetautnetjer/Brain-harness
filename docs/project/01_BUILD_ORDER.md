# 01 — Build Order

## Ordered work plan (required)
1. **Confirm retrieval baseline**
   - Done condition: deterministic-first routing behavior is validated via tests and/or controlled fixtures.
   - Non-goal: full production retrieval rollout.
2. **Seed tag registry from actual usage**
   - Done condition: candidate tags are harvested from real docs/fixtures/logs and reviewed for canonicalization.
   - Non-goal: speculative taxonomy expansion.
3. **Dry-run canonical chunk migration**
   - Done condition: v2 DDL + transform validation executed against fixtures/sandbox DB with audit output.
   - Non-goal: irreversible cutover without rollback checks.
4. **Narrow agent ownership boundaries**
   - Done condition: explicit responsibility boundaries captured and respected in prompts/manifests/docs.
   - Non-goal: broad agent runtime rewrites.
5. **Broader runtime wiring after stability**
   - Done condition: prior steps stable; only then wire wider integrations.
   - Non-goal: skipping baseline hardening.
