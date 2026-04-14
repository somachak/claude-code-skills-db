# Claude Code Skills DB

A user-friendly, installable skill library for developers using Claude Code, backed by a source-based skills database and organized into real category folders with `SKILL.md` files.

## Repo structure

- `skills/` — installable skill folders grouped by category
- `bundles/` — zip downloads for each category plus one full library bundle
- `skills-database.json` — source-backed database used to generate the library
- `skills-schema.json` — schema for the database
- `daily-update-playbook.md` — guidance for recurring updates
- `scripts/` — validation and Git sync helpers

## How to use

### Browse in GitHub

Open the `skills/` folder and then choose a category such as `frontend`, `backend`, or `testing`.

### Install manually

Copy any skill folder into one of these Claude Code skill locations:

- `~/.claude/skills/<skill-name>/SKILL.md` for personal use
- `.claude/skills/<skill-name>/SKILL.md` for project use

These locations and the `SKILL.md` entrypoint follow the official Claude Code skill structure [Claude Code Docs](https://code.claude.com/docs/en/skills).

### Download bundles

Use the zip files in `bundles/` if you want a grouped pack instead of copying one folder at a time.

## Skill categories

### AI Productivity Skills

Skills for extracting reusable skills, reviewing PRs, planning multi-agent work, building RAG-ready docs, and cataloging patterns.

- `building-rag-ready-docs` — Restructures documentation for retrieval quality with chunk-friendly sections, explicit metadata, and stable terminology. Use when preparing codebase docs, runbooks, or API guides for AI systems.
- `cataloging-codebase-patterns` — Catalogs recurring codebase patterns, preferred implementations, and anti-patterns so future skills and prompts can reference real repository behavior. Use when onboarding to large codebases or consolidating conventions.
- `curating-team-conventions` — Curates coding conventions, architectural defaults, and review standards into structured reference material that can later become skills. Use when teams repeat style, design, or workflow guidance.
- `evaluating-tooling-choices` — Evaluates libraries, frameworks, and platform choices using adoption fit, migration cost, risk, and operational burden. Use when deciding between tools for frontend, backend, testing, or infrastructure work.
- `extracting-reusable-skills` — Turns repeated successful workflows into reusable skills with proper names, descriptions, support files, and evaluation ideas. Use when recurring tasks reveal stable patterns worth codifying.
- `generating-pr-reviews` — Reviews pull requests for correctness, risk, test gaps, migration impact, and maintainability. Use when preparing PR feedback, self-reviewing changes, or training reviewers.
- `planning-multi-agent-work` — Plans work decomposition, task boundaries, handoffs, and validation points for multi-agent development workflows. Use when parallelizing large refactors, research, or incident investigations.
- `turning-runbooks-into-skills` — Converts operational runbooks into reusable skills with standing instructions, validator loops, and safe invocation controls. Use when a manual checklist is repeated often enough to automate guidance.

### Backend Skills

Skills for APIs, auth, jobs, services, concurrency, webhooks, event-driven systems, and backend documentation.

- `building-background-jobs` — Designs reliable background jobs, retry logic, scheduling strategy, idempotency, and failure handling. Use when adding workers, task queues, cron-style jobs, or async processing pipelines.
- `building-event-driven-services` — Designs event-driven services with explicit contracts, delivery semantics, replay handling, and consumer isolation. Use when adopting queues, streams, outbox patterns, or domain events.
- `designing-graphql-apis` — Designs GraphQL schemas, resolver boundaries, batching, and authorization rules. Use when building graphs, federated services, or resolver-heavy integrations.
- `designing-rest-apis` — Designs REST APIs with clear resource boundaries, versioning rules, pagination, idempotency, and error contracts. Use when creating or refactoring HTTP services and public or internal APIs.
- `documenting-api-contracts` — Produces concise API contract documentation, examples, and change notes that stay aligned with code. Use when shipping endpoints, SDKs, integrations, or internal platform surfaces.
- `handling-webhooks` — Builds and reviews webhook consumers for signature verification, retries, deduplication, ordering issues, and replay safety. Use when integrating payment, messaging, or external event providers.
- `hardening-file-uploads` — Secures file upload flows for validation, scanning, storage isolation, content-type trust, and post-processing safety. Use when handling avatars, attachments, imports, or user-generated media.
- `implementing-auth-flows` — Implements authentication and authorization flows across sessions, tokens, roles, and privileged actions. Use when shipping login, SSO, OAuth, password reset, invitation, or RBAC features.
- `reviewing-backend-concurrency` — Reviews concurrent backend code for race conditions, deadlocks, ordering bugs, lock contention, and inconsistent side effects. Use when services coordinate shared state, workers, or high-throughput workloads.
- `reviewing-caching-strategies` — Reviews cache key design, invalidation strategy, TTL choices, layering, and stale-read risks. Use when introducing Redis, CDN, query, or application-level caching.

### Data Skills

Skills for schema design, SQL review, migrations, search/indexing, analytics instrumentation, and ETL validation.

- `designing-database-schemas` — Designs relational schemas, keys, constraints, and normalization tradeoffs for operational systems. Use when creating new tables, domain models, or storage-backed product features.
- `designing-search-and-indexes` — Designs search schemas, indexing strategies, ranking tradeoffs, and query filters. Use when implementing application search, faceting, vector or lexical retrieval, or hybrid discovery features.
- `modeling-analytics-events` — Models analytics events, naming conventions, user properties, and event contracts for trustworthy product analysis. Use when adding instrumentation to frontend or backend product flows.
- `planning-data-migrations` — Plans safe schema and data migrations with backfills, rollout sequencing, rollback paths, and runtime compatibility checks. Use when changing live data models or moving data between stores.
- `reviewing-sql-performance` — Reviews SQL queries for plan quality, indexing opportunities, cardinality traps, and unnecessary scans. Use when queries slow down APIs, jobs, dashboards, or analytics pipelines.
- `validating-etl-pipelines` — Validates ETL and ELT pipelines for freshness, schema drift, lineage breaks, duplication, and reconciliation errors. Use when building ingestion jobs, warehouse transforms, or sync systems.

### Frontend Skills

Skills for UI architecture, accessibility, CSS systems, responsive behavior, bundle performance, and browser-facing security.

- `building-accessible-ui` — Reviews interface code for accessibility issues, semantic structure, keyboard behavior, focus management, and interaction risks. Use when building or reviewing component libraries, forms, dialogs, navigation, and responsive interfaces.
- `debugging-react-rendering` — Diagnoses unnecessary renders, stale closures, memoization mistakes, and state propagation issues in React applications. Use when UI feels slow, renders are noisy, or component updates are confusing.
- `designing-component-systems` — Designs reusable UI component systems, prop APIs, composition rules, and state boundaries. Use when creating or refactoring design systems, shared UI packages, or component libraries.
- `hardening-forms-and-validation` — Strengthens form UX, validation rules, error states, async submission behavior, and client-server contract alignment. Use when shipping login, checkout, onboarding, profile, or settings forms.
- `modern-css-architecture` — Improves CSS architecture, token usage, layout consistency, and responsive styling strategy. Use when refactoring styling systems, Tailwind conventions, CSS modules, or shared UI foundations.
- `optimizing-bundle-performance` — Finds bundle growth, heavy dependencies, route-splitting opportunities, and hydration risks. Use when load time, bundle size, or interaction latency becomes a concern.
- `reviewing-frontend-security` — Reviews browser-facing code for XSS, token exposure, unsafe rendering, insecure storage, and client-side trust mistakes. Use when handling user content, auth state, embeds, or rich text.
- `verifying-responsive-layouts` — Checks breakpoint behavior, overflow, spacing collapse, and layout resilience across screen sizes. Use when shipping pages, dashboards, marketing sites, or mobile-heavy workflows.

### Platform Skills

Skills for CI/CD, containers, infrastructure as code, monorepos, release workflows, and developer experience.

- `hardening-ci-pipelines` — Improves CI pipelines for speed, reliability, caching, matrix strategy, and failure isolation. Use when builds are slow, flaky, expensive, or hard to trust.
- `improving-developer-experience` — Improves local setup, scripts, docs, task runners, and onboarding paths for faster developer flow. Use when repos are hard to bootstrap, inconsistent, or slow to work in.
- `maintaining-monorepos` — Maintains monorepos through workspace boundaries, task graph design, ownership rules, and incremental validation. Use when scaling packages, apps, services, and shared libraries together.
- `managing-infrastructure-as-code` — Reviews infrastructure code for modularity, environment separation, drift risk, secret handling, and safe rollout patterns. Use when working with Terraform, Pulumi, or cloud templates.
- `running-release-checklists` — Runs release preparation checklists covering quality gates, migrations, rollback readiness, communication, and post-release verification. Use when preparing staging or production releases.
- `shipping-containerized-services` — Packages services for containers with lean images, safe defaults, environment strategy, and deployment readiness checks. Use when containerizing APIs, workers, or internal tools.

### Security and Reliability Skills

Skills for threat modeling, secrets/config audits, observability, SLOs, failure modes, and recovery readiness.

- `auditing-secrets-and-config` — Audits secret handling, environment configuration, rotation practices, and accidental exposure risks. Use when reviewing repositories, deployment configs, CI, or incident follow-up.
- `improving-observability` — Improves logging, metrics, tracing, and diagnostic context for faster debugging and healthier operations. Use when incidents are hard to diagnose or system behavior is opaque.
- `reviewing-failure-modes` — Reviews how systems fail under dependency outages, partial writes, retries, and degraded states. Use when services coordinate remote calls, queues, or critical transactions.
- `setting-slos-and-alerts` — Designs service-level objectives, indicators, and actionable alerts that reduce noise and improve operational focus. Use when tuning monitoring for APIs, background systems, or customer-facing journeys.
- `threat-modeling-features` — Threat-models new features by identifying assets, trust boundaries, attack paths, and mitigations. Use when reviewing auth changes, payments, admin tools, integrations, or other sensitive workflows.
- `validating-backup-and-restore` — Validates backup scope, recovery steps, restore drills, and data integrity assumptions. Use when services store critical operational or customer data.

### Testing Skills

Skills for unit, integration, E2E, snapshot, coverage, and production-bug regression workflows.

- `designing-integration-tests` — Designs integration tests around service contracts, persistence, side effects, and environment setup. Use when changes cross module, network, storage, or framework boundaries.
- `generating-unit-tests` — Generates focused unit tests around branches, edge cases, and regressions without overfitting to implementation details. Use when extending logic, fixing bugs, or improving confidence in isolated modules.
- `reproducing-bugs-from-logs` — Turns logs, traces, and error reports into concrete reproduction steps and regression tests. Use when investigating production failures, support tickets, or intermittent defects.
- `reviewing-test-coverage` — Reviews what is not tested and prioritizes the highest-risk missing scenarios. Use when shipping new code, after large refactors, or after incidents that revealed blind spots.
- `snapshot-regression-checks` — Applies snapshot and golden-file testing carefully for stable outputs such as APIs, emails, rendered templates, and serialization. Use when outputs should remain consistent over time.
- `stabilizing-e2e-tests` — Improves end-to-end tests by removing flakiness, clarifying waits, and aligning assertions with user-visible outcomes. Use when browser tests are brittle or slow.

## Notes

The repository uses official Claude Code skill guidance for skill structure, metadata, and discovery [Claude Code Docs](https://code.claude.com/docs/en/skills). The naming, description style, supporting-file structure, and iterative authoring approach are also aligned with Anthropic's best-practices guide [Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
