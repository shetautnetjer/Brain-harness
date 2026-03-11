# Source Documentation Pack

This source-doc pack is a compact orientation and doctrine layer built from **current repository evidence** (code, contracts, scripts, tests, manifests) plus settled project rules provided for this repository.

## Purpose
- Help future agents bootstrap quickly without inventing missing runtime behavior.
- Keep doctrine visible while preserving the distinction between verified implementation vs policy intent.
- Provide a stable starting point for narrow, additive patches.

## Authority model
1. **Live code + contracts + tests are implementation authority.**
2. **Source-doc pack files summarize and organize that authority.**
3. **When docs and code conflict, code/tests/contracts win for implementation truth.**

## Scope note
This pack intentionally avoids broad redesign. It documents what is verifiable now, calls out uncertainties explicitly, and marks migration targets as targets (not completed runtime behavior).
