# Testing Skills

Skills for unit, integration, E2E, snapshot, coverage, and production-bug regression workflows.

## Included skills

- `designing-integration-tests` — Designs integration tests around service contracts, persistence, side effects, and environment setup. Use when changes cross module, network, storage, or framework boundaries.
- `generating-unit-tests` — Generates focused unit tests around branches, edge cases, and regressions without overfitting to implementation details. Use when extending logic, fixing bugs, or improving confidence in isolated modules.
- `reproducing-bugs-from-logs` — Turns logs, traces, and error reports into concrete reproduction steps and regression tests. Use when investigating production failures, support tickets, or intermittent defects.
- `reviewing-test-coverage` — Reviews what is not tested and prioritizes the highest-risk missing scenarios. Use when shipping new code, after large refactors, or after incidents that revealed blind spots.
- `snapshot-regression-checks` — Applies snapshot and golden-file testing carefully for stable outputs such as APIs, emails, rendered templates, and serialization. Use when outputs should remain consistent over time.
- `stabilizing-e2e-tests` — Improves end-to-end tests by removing flakiness, clarifying waits, and aligning assertions with user-visible outcomes. Use when browser tests are brittle or slow.
