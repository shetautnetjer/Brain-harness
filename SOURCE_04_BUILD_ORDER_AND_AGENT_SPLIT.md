# SOURCE 04 — Build Order and Agent Split

## Required work order
1. Confirm retrieval baseline.
2. Seed tag registry from actual usage.
3. Dry-run canonical chunk migration.
4. Narrow agent ownership boundaries.
5. Broader runtime wiring only after baseline stability.

## Agent split (doctrine + repo support)
- **Jabari**: retrieval hardening/integration follow-ons (supported by retrieval-related manifests and role context).
- **Heru**: inventory and mismatch audit (supported by `prompts/heru/inventory_auditor_prompt.md`, but live runtime integration should be treated as partial until verified).
- **Kimi**: clean Plane B fixtures and canonical shaping (supported by `prompts/kimi/canonical_writer_prompt.md`; doctrine says sole Plane B writer).
- **Arbiter**: doctrine/tags/admission/violation ratification (supported by arbiter prompt and governance contracts).

## Guardrails
- Keep Plane A vs Plane B separation intact.
- Keep patches narrow and additive.
- Do not broaden runtime coupling before deterministic baseline checks pass.
