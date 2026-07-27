# Security and Reliability Skills

Threat modeling, secrets/config audits, observability, SLOs, failure modes, and recovery readiness.

## Included skills

- [`adversarial-code-review/`](./adversarial-code-review/) — Forces genuine critical code review through three hostile personas — Saboteur, New Hire, and Security Auditor — each required to find at least one real issue.
- [`audit-context-building/`](./audit-context-building/) — Builds ultra-granular architectural context through systematic line-by-line code analysis before vulnerability hunting.
- [`auditing-secrets-and-config/`](./auditing-secrets-and-config/) — Audits secret handling, environment configuration, rotation practices, and accidental exposure risks.
- [`auditing-unit-consistency/`](./auditing-unit-consistency/) — Apply dimensional analysis to application code: assign units (cents, ms, percent, tokens) to every quantity, propagate them through arithmetic, and flag dimensionally impossible operations.
- [`authoring-semgrep-rules/`](./authoring-semgrep-rules/) — Writes, tests, and ships custom Semgrep rules that catch project-specific security bugs and anti-patterns in TypeScript, Node, Python, FastAPI, and Django codebases.
- [`differential-review/`](./differential-review/) — Security-focused differential review of code changes (PRs, commits, diffs).
- [`improving-observability/`](./improving-observability/) — Improves logging, metrics, tracing, and diagnostic context for faster debugging and healthier operations.
- [`insecure-defaults/`](./insecure-defaults/) — Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production.
- [`managing-secrets-infrastructure/`](./managing-secrets-infrastructure/) — Designs and audits secrets infrastructure at scale: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager.
- [`reviewing-failure-modes/`](./reviewing-failure-modes/) — Reviews how systems fail under dependency outages, partial writes, retries, and degraded states.
- [`running-chaos-experiments/`](./running-chaos-experiments/) — Plans and runs disciplined chaos experiments against Node, FastAPI, and Django services: defining steady state, sizing blast radius, choosing fault injection tools, and writing the abort criteria before the experiment starts.
- [`scanning-with-codeql/`](./scanning-with-codeql/) — Sets up CodeQL on TypeScript/JavaScript and Python repositories to find injection bugs, auth bypasses, and unsafe deserialization that pattern-based linters miss.
- [`semgrep-rule-creator/`](./semgrep-rule-creator/) — Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns.
- [`setting-slos-and-alerts/`](./setting-slos-and-alerts/) — Designs service-level objectives, indicators, and actionable alerts that reduce noise and improve operational focus.
- [`sharp-edges/`](./sharp-edges/) — Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mistakes.
- [`threat-modeling-features/`](./threat-modeling-features/) — Threat-models new features by identifying assets, trust boundaries, attack paths, and mitigations.
- [`validating-backup-and-restore/`](./validating-backup-and-restore/) — Validates backup scope, recovery steps, restore drills, and data integrity assumptions.
