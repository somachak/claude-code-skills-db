# Launch Readiness Checklist

> Auto-generated from `skills-database.json` v2026-04-23 · 2026-04-23
> Filter: stages=['harden', 'launch']  priority=['core', 'supporting']
> **35 skills** across 2 stages

Copy this checklist into your project. Check off each skill as you apply it.
Re-run `python3 tools/generate_launch_readiness.py` to regenerate after library updates.

## 🛡️ Harden — Pre-ship: security, edge cases, coverage
*25 skills*

### Ai Productivity

- [ ] 🔑 **`generating-pr-reviews`** — Reviews pull requests for correctness, risk, test gaps, migration impact, and maintainability. Use w

### Backend

- [ ] 🔑 **`hardening-file-uploads`** — Secures file upload flows for validation, scanning, storage isolation, content-type trust, and post-
- [ ] 🔑 **`reviewing-backend-concurrency`** — Reviews concurrent backend code for race conditions, deadlocks, ordering bugs, lock contention, and 

### Data

- [ ] 🔑 **`validating-etl-pipelines`** — Validates ETL and ELT pipelines for freshness, schema drift, lineage breaks, duplication, and reconc

### Frontend

- [ ] 🔑 **`debugging-react-rendering`** — Diagnoses unnecessary renders, stale closures, memoization mistakes, and state propagation issues in
- [ ] 🔑 **`hardening-forms-and-validation`** — Strengthens form UX, validation rules, error states, async submission behavior, and client-server co
- [ ] 🔑 **`reviewing-frontend-security`** — Reviews browser-facing code for XSS, token exposure, unsafe rendering, insecure storage, and client-
- [ ] 🔑 **`verifying-responsive-layouts`** — Checks breakpoint behavior, overflow, spacing collapse, and layout resilience across screen sizes. U
- [ ]    **`avoiding-nextjs-app-router-anti-patterns`** — Identifies and fixes common Next.js 14/15 App Router anti-patterns: misuse of useEffect for data fet

### Security Reliability

- [ ] 🔑 **`auditing-secrets-and-config`** — Audits secret handling, environment configuration, rotation practices, and accidental exposure risks
- [ ] 🔑 **`reviewing-failure-modes`** — Reviews how systems fail under dependency outages, partial writes, retries, and degraded states. Use
- [ ] 🔑 **`threat-modeling-features`** — Threat-models new features by identifying assets, trust boundaries, attack paths, and mitigations. U
- [ ]    **`adversarial-code-review`** — Forces genuine critical code review through three hostile personas — Saboteur, New Hire, and Securit
- [ ]    **`audit-context-building`** — Builds ultra-granular architectural context through systematic line-by-line code analysis before vul
- [ ]    **`authoring-semgrep-rules`** — Writes, tests, and ships custom Semgrep rules that catch project-specific security bugs and anti-pat
- [ ]    **`differential-review`** — Security-focused differential review of code changes (PRs, commits, diffs). Adapts analysis depth to
- [ ]    **`insecure-defaults`** — Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow a
- [ ]    **`semgrep-rule-creator`** — Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns
- [ ]    **`sharp-edges`** — Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mist

### Testing

- [ ] 🔑 **`reproducing-bugs-from-logs`** — Turns logs, traces, and error reports into concrete reproduction steps and regression tests. Use whe
- [ ] 🔑 **`reviewing-test-coverage`** — Reviews what is not tested and prioritizes the highest-risk missing scenarios. Use when shipping new
- [ ] 🔑 **`snapshot-regression-checks`** — Applies snapshot and golden-file testing carefully for stable outputs such as APIs, emails, rendered
- [ ] 🔑 **`stabilizing-e2e-tests`** — Improves end-to-end tests by removing flakiness, clarifying waits, and aligning assertions with user
- [ ]    **`designing-property-based-tests`** — Identifies code patterns where property-based testing produces stronger coverage than example-based 
- [ ]    **`property-based-testing`** — Provides guidance for property-based testing across multiple languages and smart contracts. Use when

## 🚀 Launch — Ship mechanics: CI/CD, containers, release
*10 skills*

### Data

- [ ] 🔑 **`planning-data-migrations`** — Plans safe schema and data migrations with backfills, rollout sequencing, rollback paths, and runtim

### Platform

- [ ] 🔑 **`hardening-ci-pipelines`** — Improves CI pipelines for speed, reliability, caching, matrix strategy, and failure isolation. Use w
- [ ] 🔑 **`running-release-checklists`** — Runs release preparation checklists covering quality gates, migrations, rollback readiness, communic
- [ ] 🔑 **`shipping-containerized-services`** — Packages services for containers with lean images, safe defaults, environment strategy, and deployme
- [ ]    **`docker-optimization`** — Optimizes Dockerfiles and docker-compose configurations for image size, build speed, layer caching, 
- [ ]    **`release-lifecycle-manager`** — Manages the full software release lifecycle: semantic versioning, conventional commits, automated ch

### Security Reliability

- [ ] 🔑 **`improving-observability`** — Improves logging, metrics, tracing, and diagnostic context for faster debugging and healthier operat
- [ ] 🔑 **`setting-slos-and-alerts`** — Designs service-level objectives, indicators, and actionable alerts that reduce noise and improve op
- [ ] 🔑 **`validating-backup-and-restore`** — Validates backup scope, recovery steps, restore drills, and data integrity assumptions. Use when ser
- [ ]    **`managing-secrets-infrastructure`** — Designs and audits secrets infrastructure at scale: HashiCorp Vault, AWS Secrets Manager, Azure Key 

---

**Key:** 🔑 = core priority (must-apply) · unmarked = supporting (apply if relevant)

Generated by `tools/generate_launch_readiness.py` from `skills-database.json` v2026-04-23
