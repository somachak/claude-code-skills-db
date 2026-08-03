# Hunter Changelog

Append-only log of every daily run. Every decision the hunter makes — create, overwrite, skip, reject — is logged here with its score so a human can audit the library's evolution after the fact.

## 2026-07-20 [opus-4.6] NO-OP — +0 new / ~0 updated

Mode: full discovery + Opus quality gate. Discovered **1015 candidates** (10 GitHub searches + 4 curated repos + 3 RSS feeds; 2 RSS feeds live, anthropic news feed 404). Heuristic flagged **161 create / 0 overwrite / 3 skip / 851 reject**. After the human-grade gate: **0 accepted, 161 rejected/skipped.** No library commit — audit trail only.

Same structural over-flagging as prior runs: the heuristic's uniqueness dimension scores on candidate name/title similarity, not body-level overlap, so it scored known duplicates as `un10` (net-new). Of the 161:

### Rejected wholesale — not authored skills (92 candidates)
92 came from GitHub *repo* search and carry a README body, not a `SKILL.md` with frontmatter — they fail authoring-compliance (dimension 2) by construction. These are either curated awesome-lists (`awesome-python`, `awesome-go`, `awesome-mac`, `awesome-selfhosted`, `awesome-mcp-servers`, `awesome-llm-apps`, `awesome-nlp`, `awesome-neovim`, `awesome-quant`, `awesome-artificial-intelligence`, `free-for-dev`, `coding-interview-university`, `professional-programming`) or projects whose README is not a skill (`firecrawl`, `spec-kit`, `open-saas`, `superpowers`, `gstack`, `cc-switch`, `ruview`, `deepcode`, `deeptutor`, plus ~60 small low-signal `*-skill`/`*-kit` repos). Reject on dimension 2.

### Skipped — duplicate territory already in DB (69 curated SKILL.md)
The incumbent library was seeded from these same trailofbits/anthropics sources, so nearly every curated candidate maps to an existing skill: `semgrep-rule-creator`→**semgrep-rule-creator**; `semgrep-rule-variant-creator`→**authoring-semgrep-rules**; `codeql`→**scanning-with-codeql**; `audit-context-building`→**audit-context-building**; `adversarial-reviewer`→**adversarial-code-review**; `chaos-engineering`→**running-chaos-experiments**; `docker-development`→**docker-optimization**; `modern-python`→**configuring-modern-python-projects**; `claude-api`→**claude-api**; `ask-questions-if-underspecified`→**asking-clarifying-questions**; `spec-driven-workflow`/`spec-to-repo`→**spec-driven-development**; `llm-cost-optimizer`→**optimizing-llm-spend**; `secrets-vault-manager`→**managing-secrets-infrastructure**; `handoff`→**writing-session-handoffs**.

### Rejected — off-stack (trailofbits + alirezarezvani)
- Blockchain smart-contract security: `algorand/cairo/solana/substrate/ton-vulnerability-scanner`, `spec-to-code-compliance`.
- Systems / malware / formal methods: `c-review`, `rust-review`, `address-sanitizer`, `yara-rule-authoring`, `crypto-protocol-diagram`, `mermaid-to-proverif`, `vector-forge`, `dimensional-analysis`, `red-team`.
- `kubernetes-operator` — **reconsidered as a possible accept this run** (genuinely high-quality: reconcile-loop correctness, finalizers, status subresource, CRD/RBAC design, OperatorHub capability levels; and net-new — no k8s skill in the library). I drafted a rewritten entry, then **re-rejected to honor the 2026-07-06 precedent**: operator authoring is Go/controller-runtime, off the React/Node/Python web stack, and `platform` is not one of the three always-on categories (security-reliability, ai-productivity, testing). Consistency with the prior documented judgment wins over a one-off reversal. If the maintainer wants Go/infra authoring in scope, that's a stack-gate change to make deliberately, not silently.
- `testing-handbook-generator`, `diagramming-code` — meta/generic; no decision framework beyond what Claude already knows.

### Rejected — off-scope role/business skills (alirezarezvani)
Business/ops (`capacity-planner`, `internal-comms`, `knowledge-ops`, `process-mapper`, `procurement-optimizer`, `vendor-management`, `channel-economics`, `partnerships-architect`, `pricing-strategist`, `chief-ai-officer-advisor`), marketing (`ab-test-setup`, `churn-prevention`, `copy-editing`, `free-tool-strategy`, `onboarding-cro`, `pricing-strategy`), medical/research (`fda-consultant-specialist`, `risk-management-specialist`, `clinical-research`, `market-research`, `product-research`, `research-finance`), broad role prompts (`senior-fullstack`, `senior-devops`, `azure-cloud-architect`, `gcp-cloud-architect`, `behuman`), and novelties (`interpreting-culture-index`, `let-fate-decide`, `genotoxic`, `graph-evolution`).

Net: library unchanged at 80 skills. The candidate pool is now saturated against a mature library; future net-new value will require new sources or a deliberate stack-gate widening.

## 2026-07-06 [opus-4.6] NO-OP — +0 new / ~0 updated

Mode: full discovery + Opus 4.6 quality gate. Discovered **969 candidates** (10 GitHub searches + 4 curated repos + 3 RSS feeds). Heuristic flagged **160 create / 0 overwrite / 3 skip / 806 reject**. After applying the human-grade quality gate: **0 accepted, 160 rejected/skipped.** No commit to the skills library — audit trail only.

The heuristic over-flags because its uniqueness dimension scores on candidate name/title/description similarity, not body-level overlap with the incumbent library. Every flagged "create" fell into one of four buckets:

### Skipped — duplicate territory already in DB (17 curated SKILL.md)
- `claude-api` → **claude-api** (same anthropics source; incumbent faithful)
- `ask-questions-if-underspecified` → **asking-clarifying-questions** / **clarifying-underspecified-requests**
- `audit-context-building` → **audit-context-building** (created 2026-04-23)
- `modern-python` → **configuring-modern-python-projects**
- `semgrep-rule-creator` → **semgrep-rule-creator**; `semgrep-rule-variant-creator` → **authoring-semgrep-rules**
- `codeql` → **scanning-with-codeql**
- `adversarial-reviewer` → **adversarial-code-review** (created 2026-04-23)
- `chaos-engineering` → **running-chaos-experiments**
- `docker-development` → **docker-optimization** (created 2026-04-23)
- `llm-cost-optimizer` → **optimizing-llm-spend**
- `secrets-vault-manager` → **managing-secrets-infrastructure** (created 2026-04-23)
- `spec-driven-workflow` / `spec-to-repo` → **spec-driven-development**
- `handoff` → **writing-session-handoffs**
- `codebase-onboarding` → **cataloging-codebase-patterns** (also thin, 2.2k chars)

### Rejected — off-stack (trailofbits + alirezarezvani)
- Blockchain: `algorand/cairo/solana/substrate/ton-vulnerability-scanner`, `spec-to-code-compliance`, `dimensional-analysis`, `vector-forge`, `crypto-protocol-diagram`, `mermaid-to-proverif`
- Systems languages: `c-review`, `rust-review`, `address-sanitizer`, `yara-rule-authoring` (C/C++/malware)
- `kubernetes-operator` — genuinely high-quality (reconcile-loop correctness, finalizers, CRD/RBAC design, OperatorHub capability levels) but niche Go/controller-runtime infra authoring; off the React/Node/Python web stack and not an always-on category. Reject on stack-relevance, not quality.
- `red-team` — offensive-security engagement planning (MITRE ATT&CK kill-chains, OPSEC, crown-jewel targeting). Cross-refs pentest/threat-detection/IR skills absent from this library; it's security-operations, not web-appsec. Off-stack.
- `diagramming-code` — generic mermaid-from-code utility; content Claude already knows, no decision framework. Reject on depth/genericness.

### Rejected — off-scope role/business skills (alirezarezvani)
- Business/ops: `capacity-planner`, `internal-comms`, `knowledge-ops`, `process-mapper`, `procurement-optimizer`, `vendor-management`, `channel-economics`, `partnerships-architect`, `pricing-strategist`, `chief-ai-officer-advisor`
- Marketing (previously rejected): `ab-test-setup`, `churn-prevention`, `copy-editing`, `free-tool-strategy`, `onboarding-cro`, `pricing-strategy`, `experiment-designer`
- Medical/research: `fda-consultant-specialist`, `risk-management-specialist`, `clinical-research`, `market-research`, `product-research`, `research-finance`
- Broad role descriptions (like previously-rejected senior-devops): `senior-fullstack`, `senior-devops`, `azure-cloud-architect`, `gcp-cloud-architect`, `behuman`
- Off-scope novelties: `interpreting-culture-index` (HR), `let-fate-decide` (tarot), `genotoxic` / `graph-evolution` (bio), `testing-handbook-generator` (meta-skill)

### Rejected — 91 bare-repo README candidates (not executable skills)
awesome-lists (`awesome-python`, `awesome-go`, `awesome-selfhosted`, `awesome-llm-apps`, `awesome-mcp-servers`, `awesome-quant`, `awesome-neovim`, `awesome-nlp`, `awesome-web-security`, `awesome-agent-skills`, `awesome-openclaw-skills`, …), knowledge repos (`coding-interview-university`, `professional-programming`), tool/app READMEs (`firecrawl`, `browser-use`, `spec-kit`, `encore`, `cc-switch`), and starter templates / SEO-manufactured skill orgs (`open-saas`, `gstack`, `skybridge`, `agency-agents`, `ai-website-cloner-template`, `code-review-skill`, `ui-ux-pro-max-skill`, `styleseed`, `oh-my-design`, `lovcode`, …). None ship a standalone quality SKILL.md body.

### Discovery failure modes
- RSS feeds 403 as always (medium.com/feed/tag/claude-code, medium.com/feed/tag/anthropic, anthropic.com/news/rss.xml).
- X / Exa queries skipped (no X_BEARER_TOKEN / EXA_API_KEY).
- GitHub core/search rate limits healthy (5000 / 30 remaining). Discovery is slow (~200 sequential raw fetches) but completed via warm cache.

**Net: the curated sources (anthropics, trailofbits, alirezarezvani) are fully mined by prior runs; no net-new, stack-relevant, non-duplicate, high-quality skill surfaced today. Library unchanged at 79 skills.**

## 2026-04-23 [opus-4.6] APPLIED — +6 new / ~0 updated

Mode: full discovery + Opus 4.6 quality gate. Discovered 716 candidates (github search + 4 curated repos + 3 RSS feeds). Heuristic flagged 119 creates. After quality gate: 6 accepted, 113 rejected, 0 overwrites.

### Created (6)

- [create] `audit-context-building` score=78
  source=https://github.com/trailofbits/skills/blob/main/plugins/audit-context-building/skills/audit-context-building/SKILL.md
  reason=Genuinely net-new. Five-phase pre-audit context methodology (orientation, ultra-granular function analysis, global state reconstruction, stability rules, integration) has zero overlap with any existing skill. Security-reliability always-on. Rewrote for stack-agnostic dev audience, removed blockchain-specific framing from original.

- [create] `spec-driven-development` score=76
  source=https://github.com/alirezarezvani/claude-skills/blob/main/engineering/spec-driven-workflow/SKILL.md
  reason=Net-new. Nine-section spec template + six-phase workflow + bounded autonomy rules directly addresses AI-agent over-implementation. No existing skill covers spec-first methodology. Similarity to designing-workflow-skills (meta-skill) is <0.35 (different domain). ai-productivity always-on category.

- [create] `docker-optimization` score=74
  source=https://github.com/alirezarezvani/claude-skills/blob/main/engineering/docker-development/SKILL.md
  reason=Net-new vs shipping-containerized-services (deployment readiness) and hardening-ci-pipelines (pipeline). Docker-optimization is specifically about Dockerfile authoring — multi-stage builds, layer caching, base image selection, .dockerignore, security hardening. Different scope, trigram similarity ~0.20. Platform category.

- [create] `managing-secrets-infrastructure` score=76
  source=https://github.com/alirezarezvani/claude-skills/blob/main/engineering/secrets-vault-manager/SKILL.md
  reason=Net-new vs auditing-secrets-and-config (which audits code-level practices). This skill is infrastructure: Vault HA setup, dynamic credentials, rotation automation, CI/CD OIDC integration, 15-minute emergency procedure. Trigram similarity ~0.18. Security-reliability always-on.

- [create] `adversarial-code-review` score=80
  source=https://github.com/alirezarezvani/claude-skills/blob/main/engineering-team/adversarial-reviewer/SKILL.md
  reason=Net-new. Three hostile personas with mandatory-finding rule and severity amplification is a distinct methodology from generating-pr-reviews (collaborative) and differential-review (security regression). Self-review blind-spot elimination fills a real gap. Trigram similarity to incumbents ~0.22. Security-reliability category.

- [create] `release-lifecycle-manager` score=74
  source=https://github.com/alirezarezvani/claude-skills/blob/main/engineering/release-manager/SKILL.md
  reason=Net-new vs running-release-checklists (single checklist execution). This covers semantic versioning automation, conventional commits parsing, changelog generation, hotfix SLA procedures, and rollback trigger definition. Full lifecycle scope. Platform category.

### Skipped (notable)

- `modern-python` (trailofbits) — already in DB as configuring-modern-python-projects. Trailofbits version is the source material; incumbent is faithful. Skip.
- `semgrep-rule-creator` (trailofbits overwrite) — existing semgrep-rule-creator already carries full trailofbits content at 7002 chars. No meaningful delta. Skip.
- `senior-devops` (alirezarezvani) — broad DevOps role description. Territory covered by hardening-ci-pipelines, managing-infrastructure-as-code, shipping-containerized-services. Would be duplicate, not net-new.
- `spec-to-code-compliance` (trailofbits) — blockchain-specific smart contract compliance audit. Off-stack for this library.
- `dimensional-analysis` (trailofbits) — DeFi/financial arithmetic annotation. Off-stack.
- `adversarial-reviewer` (alirezarezvani) — accepted as adversarial-code-review above with significant rewrite to meet authoring standards.

### Rejected (representative sample from 113)

- `awesome-*` (40+ repos) — resource curation lists, not executable skills
- `coding-interview-university`, `professional-programming`, `learning`, `howtheytest` — knowledge repos, not Claude skills
- `browser-use`, `playwright` (repo), `laravel`, `firecrawl`, `servers` (MCP) — tool READMEs with no SKILL.md
- `open-saas`, `codepilot`, `ai-website-cloner-template`, `skybridge`, `gstack`, `agency-agents`, `orchestkit`, `editor-pro-max`, `lovcode`, `beagle`, `silos` — starter templates or app tools with no skill body
- `code-review-skill` (awesome-skills org) — heuristic scored 90 but org looks manufactured for SEO; body similarity to generating-pr-reviews is high
- `carmack-council`, `builder-skills`, `stitch-kit`, `skillnote`, `tezgah`, `claude-agent-team-manager` — interesting but no standalone SKILL.md quality
- `algorand/cairo/solana/substrate/ton-vulnerability-scanner` — blockchain-specific, off-stack
- `yara-rule-authoring`, `address-sanitizer`, `testing-handbook-generator` — C/C++ fuzzing or meta-skill, off-stack
- `let-fate-decide`, `interpreting-culture-index` — tarot cards and HR assessment, clearly off-scope
- Marketing skills (ab-test-setup, churn-prevention, copy-editing, free-tool-strategy, onboarding-cro, pricing-strategy) — off-stack for dev-focused library
- Medical device skills (fda-consultant-specialist, risk-management-specialist) — off-stack

### Discovery failure modes

- Three RSS feeds returned 403 (medium.com/feed/tag/claude-code, medium.com/feed/tag/anthropic, anthropic.com/news/rss.xml) — same persistent failure as previous runs
- Two curated README 404s (sindresorhus/awesome, bradtraversy/design-resources-for-developers) — same as previous runs; sources.yml should be cleaned up
- Ran without GITHUB_TOKEN — GitHub API unauthenticated rate limits may have caused missing results on busy search queries
- hunter/run_hunter.py dry-run timed out at 90s due to network-heavy discovery; decision application done manually via apply_skills.py

## 2026-04-15 [opus-4.6]

Mode: manual merge (runner flagged 121 create / 0 overwrite / 592 reject from 713 discovered). Heuristic was aggressive — most flagged candidates were repo-level awesome-lists or stack-irrelevant templates, not real SKILL.md files. Applied skeptical quality gate per rubric.

### Created (3)

- `configuring-modern-python-projects` — Adapted from trailofbits/skills `modern-python`. Net-new territory (no existing Python-tooling skill). Rewrote for FastAPI/Django focus, tightened uv/ruff/ty anti-pattern table, added worked example. Score 82.
- `designing-property-based-tests` — Adapted from trailofbits/skills `property-based-testing`. Net-new (testing category, no PBT coverage). Rewrote with fast-check + Hypothesis worked examples on TS/Python; dropped smart-contract priority row (off-stack). Score 78.
- `authoring-semgrep-rules` — Adapted from trailofbits/skills `semgrep-rule-creator`. Net-new (security-reliability, always-on). Rewrote worked example around FastAPI open-redirect taint rule; kept "rationalizations to reject" framing. Score 76.

### Rejected (highlights — why the 118 other "create" flags were dropped)

- `superpowers`, `everything-claude-code`, `spec-kit`, `awesome-mcp-servers`, `awesome-llm-apps`, `awesome-go`, `awesome-selfhosted`, `awesome-neovim`, `awesome-tmux`, `awesome-claude-code`, `awesome-openclaw-skills`, `awesome-agent-skills`, `awesome-mcp-clients`, `awesome-llm-resources`, `awesome-prompts`, `free-for-dev`, `coding-interview-university`, `professional-programming`, `learning`, `howtheytest` — all repo-level awesome-lists or curation indexes, not skills.
- `browser-use`, `playwright`, `laravel`, `servers` (MCP), `firecrawl`, `lobehub`, `autoresearch` — tool repos; compliance score 0 (no SKILL.md).
- `open-saas`, `ai-website-cloner-template`, `codepilot`, `skybridge`, `ai-design-components`, `orchestkit`, `lovcode`, `agency-agents`, `editor-pro-max`, `cchub`, `beagle`, `tezgah`, `pharaohfolio`, `claude-nextjs-skills`, `claude-code-nextjs-skills`, `claude-code-python-stack`, `claude-agent-team-manager`, `builder-skills`, `stitch-kit`, `carmack-council`, `ctxvault`, `a2ui-adk`, `aegisgate`, `skillnote`, `gstack`, `zeroclaw`, `claud-skills`, `agent-skills-directory`, `creativly-ai-brand-video-remotion`, `mastering-typescript-skill`, `motion-dev-animations-skill`, `fastapi-agent-blueprint`, `fastapi-claude-template`, `software-dev-ai-claude-toolkit`, `pm-skills`, `marketing-for-founders`, `ai-coding-rules`, `antigravity-awesome-skills` — starter templates or boilerplate; no deep decision-making content.
- `skills` (anthropics/skills monorepo) — parent index, not a single skill.
- `claude-skills` (alirezarezvani) — index; individual SKILLs evaluated separately.
- `code-review-skill` (awesome-skills) — too similar to existing `generating-pr-reviews` (similarity ~0.55) and incumbent is tighter / stack-focused.
- trailofbits individual SKILLs: `ask-questions-if-underspecified`, `dimensional-analysis`, `interpreting-culture-index`, `sharp-edges`, `testing-handbook-generator`, `designing-workflow-skills`, `genotoxic`, `graph-evolution` — generic meta content or off-domain.
- `algorand-`, `cairo-`, `solana-`, `substrate-`, `ton-vulnerability-scanner`, `yara-rule-authoring`, `address-sanitizer`, `codeql`, `crypto-protocol-diagram`, `diagramming-code`, `mermaid-to-proverif`, `vector-forge`, `differential-review`, `insecure-defaults`, `let-fate-decide`, `semgrep-rule-variant-creator`, `spec-to-code-compliance`, `audit-context-building`, `claude-api` — off-stack (blockchain, C/C++ sanitizers, niche crypto) or too narrow for this library's React/Next/TS, Node, Python/FastAPI/Django focus.
- `alirezarezvani/claude-skills` individual SKILLs (adversarial-reviewer, azure/gcp-cloud-architect, red-team, senior-devops, behuman, codebase-onboarding, docker-development, release-manager, secrets-vault-manager, spec-driven-workflow, ab-test-setup, churn-prevention, copy-editing, free-tool-strategy, onboarding-cro, pricing-strategy, experiment-designer, spec-to-repo, fda-consultant-specialist, risk-management-specialist) — either generic role descriptions that overlap with existing skills (docker, release, devops, secrets all have close incumbents) or off-stack (marketing/regulatory).

### Discovery failure modes

- Three curated RSS feeds returned 403 (medium.com/feed/tag/claude-code, medium.com/feed/tag/anthropic, anthropic.com/news/rss.xml).
- Two README URLs returned 404 (sindresorhus/awesome main → README moved; bradtraversy/design-resources-for-developers).
- Ran without `GITHUB_TOKEN` / `ANTHROPIC_API_KEY` / `EXA_API_KEY` — GitHub API unauthenticated rate limits apply; enrichment of candidate bodies was manual rather than LLM-assisted.

## 2026-04-16T00:00:00Z APPLIED — +4 / ~0

Hunter run by Opus 4.6 (Cowork mode, daily-skills-hunter scheduled task).
712 candidates discovered, 120 heuristically flagged as create, 592 rejected by heuristic.

### Quality Gate (Opus 4.6 override)

Heuristic scores are badly miscalibrated — most "create" candidates are:
- awesome-* curated lists (not skills), e.g. awesome-selfhosted, awesome-mcp-servers, awesome-neovim
- General interview prep repos (coding-interview-university, professional-programming)
- Popular framework repos that are not Claude skills (laravel, playwright, browser-use)
- Template/boilerplate repos with no skill body (ai-website-cloner-template, open-saas)
- Repos that 404 on SKILL.md or README (builder-skills, stitch-kit, claud-skills)

After manual review of source content against quality_rubric.md, 4 skills were accepted:

- [create] `avoiding-nextjs-app-router-anti-patterns` score=90
  source=https://github.com/wsimmonds/claude-nextjs-skills/nextjs-anti-patterns
  reason=Real SKILL.md with anti-pattern taxonomy, code examples, decision checklist; net-new territory (no Next.js correctness skill in DB)

- [create] `implementing-postgres-vector-search` score=90
  source=https://github.com/laguagu/claude-code-nextjs-skills/skills/postgres-semantic-search
  reason=Deep pgvector + BM25 + HNSW content; genuinely distinct from generic designing-search-and-indexes; critical for RAG stack

- [create] `building-nextjs-shadcn-interfaces` score=88
  source=https://github.com/laguagu/claude-code-nextjs-skills/skills/nextjs-shadcn
  reason=Concrete Next.js 15 + shadcn/ui setup and composition rules; below-threshold similarity to existing component-systems and css-architecture skills

- [create] `animating-react-components-with-motion` score=80
  source=https://github.com/199-biotechnologies/motion-dev-animations-skill/SKILL.md
  reason=Well-structured SKILL.md with pattern decision tree, spring physics reference, accessibility rules; zero overlap with existing library

### Rejected (representative sample)

- [reject] `coding-interview-university` — interview prep repo, not a Claude skill; off-stack
- [reject] `awesome-selfhosted`, `awesome-mcp-servers`, `awesome-neovim`, etc. — resource lists, not executable skills
- [reject] `professional-programming` — 170k-char reading list, no skill structure
- [reject] `spec-kit` (github/spec-kit) — GitHub's internal spec format, not Claude skills
- [reject] `laravel` — off-stack (PHP framework repo)
- [reject] `software-dev-ai-claude-toolkit` — useful toolkit README but individual skill bodies are not standalone SKILL.md files
- [reject] `carmack-council` — innovative multi-agent Next.js/tRPC framework but requires external Vercel skill and highly stack-opinionated; body depth insufficient for standalone use
- [reject] `stitch-kit` — requires paid Google Stitch MCP API key; too service-dependent
- [reject] `browser-use`, `playwright`, `firecrawl` — popular OSS tool READMEs, not Claude skill authoring
- [reject] `ctxvault` — Python agent memory library, interesting but not a SKILL.md and off-stack
- [reject] ~108 others — below threshold, awesome-lists, editor plugins, or off-stack material


## 2026-04-22 [opus-4.6] APPLIED — +9 new / ~0 updated

Mode: full discovery + Opus quality gate. Discovered 715 candidates (github search + curated repos + RSS). Heuristic flagged 123 creates. After quality gate: 9 accepted, 114 rejected.

### Created (9)

- [create] `frontend-design` score=90
  source=https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
  reason=Official Anthropic skill — not in DB. Deep design thinking direction (brutalist/editorial/luxury aesthetics), anti-AI-slop principles, typography/motion/spatial composition guidance. Genuinely net-new territory in frontend category.

- [create] `webapp-testing` score=82
  source=https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md
  reason=Official Anthropic skill — not in DB. Playwright-focused with decision tree for static vs dynamic apps, with_server.py lifecycle management, reconnaissance-then-action workflow. Distinct from existing stabilizing-e2e-tests (that's about flaky test repair, this is about interaction automation).

- [create] `claude-api` score=88
  source=https://github.com/anthropics/skills/blob/main/skills/claude-api/SKILL.md
  reason=Official Anthropic skill — not in DB. Authoritative surface-selection framework, current model table, adaptive thinking patterns, anti-patterns, provider-detection logic. Rewrote from 32k to 5.4k retaining highest-value decision content. Always-on category (ai-productivity).

- [create] `property-based-testing` score=78
  source=https://github.com/trailofbits/skills/blob/main/plugins/property-based-testing/skills/property-based-testing/SKILL.md
  reason=Net-new despite existing designing-property-based-tests. PBT skill has property catalog, strength hierarchy, and task-typed decision tree (writing/designing/reviewing/interpreting failures). Trigram similarity 0.16 (below 0.40 threshold). Complements rather than duplicates incumbent.

- [create] `semgrep-rule-creator` score=76
  source=https://github.com/trailofbits/skills/blob/main/plugins/semgrep-rule-creator/skills/semgrep-rule-creator/SKILL.md
  reason=Net-new vs existing authoring-semgrep-rules. ToB version has "rationalizations to reject" pattern, false-positive control, taint mode worked examples, and validation loop. Trigram similarity near zero. Deeper and more opinionated than incumbent.

- [create] `sharp-edges` score=80
  source=https://github.com/trailofbits/skills/blob/main/plugins/sharp-edges/skills/sharp-edges/SKILL.md
  reason=No overlap with any existing skill. API misuse-resistance analysis is a distinct security discipline. "Pit of success" framing, JWT/crypto footgun taxonomy, rationalization rejection table. Fits security-reliability always-on category.

- [create] `differential-review` score=82
  source=https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md
  reason=Net-new. Security-focused diff review with blast-radius quantification, codebase-size strategy, and mandatory report generation. Distinct from generating-pr-reviews (general PR feedback) — this is specifically security regression detection.

- [create] `insecure-defaults` score=82
  source=https://github.com/trailofbits/skills/blob/main/plugins/insecure-defaults/skills/insecure-defaults/SKILL.md
  reason=Net-new. Fail-open vs fail-secure distinction is precise and valuable. Explicitly scoped away from test fixtures, example files, dev-only tools. Fills gap in security-reliability category.

- [create] `designing-workflow-skills` score=78
  source=https://github.com/trailofbits/skills/blob/main/plugins/workflow-skill-design/skills/designing-workflow-skills/SKILL.md
  reason=Net-new meta-skill for skill authors. Numbered phases with entry/exit criteria, description-as-trigger principle, routing patterns, safety gates. Directly applicable to anyone building Claude Code skills. Fits ai-productivity always-on category.

### Skipped (notable)

- `modern-python` (trailofbits) — DB already has strong `configuring-modern-python-projects` with identical toolset (uv/ruff/ty). ToB version adds prek and security tooling table but conceptually duplicate. Incumbent scored 80+. Skipped per no-duplicates rule.
- `theme-factory` (anthropics/skills) — DB has `artifact-stylist` covering same territory (theming artifacts). Skip.
- `testing-handbook-generator` — Meta-tool for generating other skills from ToB handbook. Too narrow/bootstrapping-only. Skip.
- `ask-questions-if-underspecified` — Useful but generic Claude behavior, not stack-specific. Score 60, compliance below threshold.

### Rejected (representative sample from 114)

- `awesome-*` (50+ repos) — Resource curation lists, not executable skills.
- `coding-interview-university`, `professional-programming` — Off-stack knowledge repos.
- `browser-use`, `playwright` (repo), `laravel`, `firecrawl` — Tool READMEs, not SKILL.md files.
- `open-saas`, `codepilot`, `ai-website-cloner-template`, `skybridge` — Starter templates; no SKILL.md depth.
- `carmack-council`, `orchestkit`, `agency-agents`, `editor-pro-max` — Interesting architectures but no standalone skill authoring quality.
- `alirezarezvani/claude-skills/*` (all at score 60) — Shallow bodies; "POWERFUL" branding with thin decision content. Compliance scores 10-15, below 15 minimum.
- `insecure-defaults-from-gstack`, `ctxvault`, `claude-agent-team-manager`, `beagle` — Below threshold.


## 2026-06-23 [opus-4.6] RECOVERY COMMIT — +7 new / ~0 updated

Backfill commit. The scheduled task has been running daily since 2026-04-23 and silently failing `git push` every time because the sandbox has no GitHub credentials. ~60 days of curation work lived only in ephemeral `/tmp` until the sandbox was wiped.

This commit restores the work that survived in two saved-to-disk patches plus today's session, deduplicating across overlapping runs.

### Recovered from disk (5)

- [recovered] `clarifying-underspecified-requests` (ai-productivity/core/experiment) — source patch `2026-05-04`
- [recovered] `optimizing-llm-spend` (ai-productivity/supporting/scale) — source patch `2026-05-25` (preferred over May 4's `optimizing-llm-api-costs` per user choice)
- [recovered] `writing-session-handoffs` (ai-productivity/supporting/build) — source patch `2026-05-25`
- [recovered] `running-chaos-experiments` (security-reliability/supporting/scale) — source patch `2026-05-25`
- [recovered] `scanning-with-codeql` (security-reliability/supporting/harden) — source patch `2026-05-25` (preferred over May 4's `running-codeql-scans`)

### Created today (2)

- [create] `asking-clarifying-questions` (ai-productivity/supporting/experiment) — 6-axis test + 1–5 question template + stack-specific hot spots. Source: trailofbits.
- [create] `managing-feature-flag-lifecycle` (platform/core/launch) — 4-type taxonomy, ring-based rollout, provider picker. Source: alirezarezvani.

### Dropped (collision resolution)

- `designing-chaos-experiments` (today, drafted in session) — dropped in favour of recovered `running-chaos-experiments`.
- `optimizing-llm-api-costs` (May 4 patch) — superseded by recovered May 25 `optimizing-llm-spend`.
- `running-codeql-scans` (May 4 patch) — superseded by recovered May 25 `scanning-with-codeql`.

### Truly lost (full bodies gone, only transcript descriptions remain)

- `2026-05-11`: `typescript-react-patterns`, `building-fastapi-clean-architecture`, `authoring-yara-rules`, `running-codeql-analysis`, `building-kubernetes-operators`.
- `2026-04-27`: `authoring-yara-detection-rules`.
- `2026-05-18` / `2026-06-01`: net zero new (all overlapped with recovered).

Possible to re-do later by re-running today's hunter on the relevant upstream repos.

### Root cause / fix

The scheduled task runs in an ephemeral sandbox with no `GITHUB_TOKEN`, no SSH key, no `gh` CLI. Every run cloned fresh from origin, made the commit, and the `git push` quietly failed. Fix: add a fine-scoped GitHub PAT to the scheduled task env and clone via `https://${GITHUB_TOKEN}@github.com/somachak/claude-code-skills-db.git`.

## 2026-07-13 [opus-4.6] APPLIED — +1 new / ~0 updated

Pipeline: 972 candidates discovered, 161 heuristic `create` flags (all scored as "net-new" by the cheap fuzzy dedup, which over-credits novelty). Applied the manual quality gate; accepted 1.

### Created (1)

- [create] `structuring-fastapi-clean-architecture` (backend/core/build) — score 82. Net-new territory: the library had backend skills (REST/GraphQL design, auth, events, concurrency) but nothing on structuring a FastAPI service into domain/application/infrastructure/presentation layers with transport-agnostic use cases. Maximal stack fit (Python/FastAPI). Body authored fresh (5,929 chars) from the clean/hexagonal pattern — not copied from source. Source signal: ocbunknown/fastapi-clean-architecture-template + corroborating vstorm-co/production-stack-skills.

### Rejected / skipped (notable)

- [skip] `modern-python` (trailofbits, real SKILL.md) — near-duplicate of incumbent `configuring-modern-python-projects`, which already covers uv/ty/ruff/PEP 723/PEP 735 with a FastAPI worked example and is MORE stack-tailored. Candidate's only delta is `prek`; does not beat incumbent by 15%.
- [skip] `motion-dev-animations-skill` (65★) — duplicate territory of incumbent `animating-react-components-with-motion` (Motion/Framer Motion for React/Next).
- [skip] `claude-api` (anthropics) — this is our existing incumbent; not a new skill.
- [reject] README-index repos with no focused body: `claude-code-nextjs-skills`, `claude-nextjs-skills`, `claude-code-python-stack`, `production-stack-skills`, `ai-design-components`, `oh-my-design`, `code-review-skill`, `styleseed` — multi-skill bundles whose contents overlap existing frontend/backend/nextjs/postgres skills; nothing net-new survives dedup.
- [reject] Heuristic noise: awesome-lists (`awesome-python`, `awesome-go`, `awesome-mcp-servers`, `awesome-selfhosted`, `free-for-dev`, `coding-interview-university`, etc.) — link collections, not skills.
- [reject] Off-stack: alirezarezvani business-ops / c-level / marketing / RA-QM skills; trailofbits blockchain vuln scanners (algorand/cairo/solana/substrate/ton) and non-stack languages (c-review, rust-review) — outside React/Next/TS, Node, Python, Tailwind/shadcn and the always-on categories.
- [reject] Stub bodies (~54 chars, README pointers not real SKILL.md): alirezarezvani `chaos-engineering`, `docker-development`, `kubernetes-operator`, `secrets-vault-manager`, `spec-driven-workflow`.

## 2026-07-27 [opus-4.6] APPLIED — +2 new / ~0 updated

Pipeline: 997 candidates discovered, 163 heuristic `create` flags, 0 overwrite. Manual quality gate accepted 2.

### Created (2)

- [create] `designing-deep-modules` (ai-productivity/core/build) — score ~85. Net-new: nothing in the library covered module/interface design (deep vs shallow, seams, adapters, deletion test, one-adapter rule, testability-through-the-interface). Rewritten from mattpocock/skills `codebase-design` (high-signal author, real SKILL.md with glossary + rejected framings); body authored fresh (4.6KB), tailored to TS/Python with deepening moves, anti-patterns, and checklist.
- [create] `auditing-unit-consistency` (security-reliability/supporting/harden) — score ~85. Net-new: no incumbent covers unit/dimension auditing of arithmetic code (cents vs dollars, ms vs s, percent vs bps, float money). Distilled from trailofbits `dimensional-analysis`; source is a multi-subagent orchestration pipeline unusable standalone, so the core technique (vocabulary → anchor annotation → propagation → red flags → validation with rationalization rejection) was rewritten (4.1KB) as a single-context skill for TS/Python app code.

### Rejected / skipped (notable)

- [skip] mattpocock `domain-modeling` — decent but thin (3.4KB), similarity 0.4–0.6 to `curating-team-conventions`/`clarifying-underspecified-requests` territory; glossary-maintenance value is modest. Candidate for supporting-file treatment later.
- [reject] mattpocock `resolving-merge-conflicts` — 921-char stub, fails depth gate.
- [reject] trailofbits `testing-handbook-generator` — meta-skill requiring their handbook repo checkout; not portable. `spec-to-code-compliance` — blockchain/whitepaper-flavored, overlaps `differential-review` + `documenting-api-contracts`. `address-sanitizer`, `c-review`, `rust-review`, blockchain vuln scanners, `yara`, `codeql` (incumbent exists), trailmark diagram skills — off-stack or duplicate.
- [reject] `ui-ux-pro-max-skill` (85) — value lives in its CSV rule datasets + scripts, not rewritable without wholesale copying; overlaps `frontend-design`/`building-nextjs-shadcn-interfaces`.
- [reject] `claude-osint` (82) — offensive recon tradecraft (dorks, credential validators); out of library scope.
- [reject] `ruview` (81) — WiFi sensing project; heuristic scored the README, pure noise. Same for `html-anything`, `skybridge`, `open-saas`, `dify`, `codepilot`, `gstack`, `spec-kit` (product READMEs, not skills; `spec-driven-development` incumbent already covers spec-kit's methodology).
- [reject] Bundles/indexes: `superpowers`, `carmack-council`, `agent-skills`, `builder-skills`, `software-dev-ai-claude-toolkit`, `anthropic-cybersecurity-skills`, `agency-agents`, `awesome-*` lists, `free-for-dev`, `coding-interview-university`, `professional-programming` — README indexes, not focused skills.
- [reject] alirezarezvani business-ops/c-level/marketing/RA-QM sub-skills (~30 flagged at 60) — off-stack, same verdict as 2026-07-13.
- Note: heuristic uniqueness scoring still over-credits novelty (163 "net-new" flags); manual gate remains essential.

## 2026-08-03 — opus-4.6 run (manual quality gate over dry-run heuristics)

Runner discovered 1003 candidates; heuristics flagged 164 create / 0 overwrite. Opus gate accepted 2, rejected/skipped the rest.

### Accepted
- **OVERWRITE `generating-pr-reviews`** ← awesome-skills/code-review-skill (1,594★, pushed 2026-07). Incumbent was 1.7k chars of generic advice; rewrite distills the source's four-phase timed process, six-level severity taxonomy, question/suggest feedback technique, reuse audit, and adds React/Next, TS/Node, Python/FastAPI/Django line-review checkpoints. Clear ≥15% improvement.
- **CREATE `enforcing-design-consistency`** (frontend) ← bitjaru/styleseed (863★, pushed 2026-07-31). Net-new territory vs `frontend-design` (creation-time aesthetics): this covers lifetime consistency — committed DESIGN.md decision lock, tokens-only rule, banned AI-look tells, 0–100 score-then-fix gate, rendered verification, cross-session drift prevention. Body rewritten, not copied.

### Skipped (adjacent but not materially better than incumbents)
- ui-ux-pro-max-skill (112k★): value lives in CSV data assets (161 rules/84 styles), not distillable into single-file form without wholesale copying; frontend-design + new consistency skill cover the actionable core.
- oh-my-design (406★): DESIGN.md installer/reference collection; method territory now covered by enforcing-design-consistency.
- claude-nextjs-skills, claude-code-nextjs-skills, fastapi-claude-template, production-stack-skills, motion-dev-animations-skill, modern-python, semgrep-rule-creator/variant, ask-questions-if-underspecified, claude-api, audit-context-building, chaos-engineering, docker-development, kubernetes-operator, secrets-vault-manager, codeql: territory already held by existing skills (nextjs anti-patterns, fastapi clean architecture, motion, configuring-modern-python-projects, semgrep×2, clarifying-underspecified-requests, claude-api, docker-optimization, running-chaos-experiments, managing-secrets-infrastructure, scanning-with-codeql).

### Rejected (with reasoning, grouped)
- Awesome/curated lists, not skills: awesome-python, awesome-go, awesome-selfhosted, awesome-mac, awesome-neovim, awesome-nlp, awesome-quant, awesome-mcp-servers, awesome-llm-apps, awesome-artificial-intelligence, free-for-dev, professional-programming, coding-interview-university, awesome-agent-skills, agentic-awesome-skills, awesome-openclaw-skills.
- Products/tools/templates whose README scored as a "skill": html-anything, firecrawl, dify, spec-kit, cc-switch, open-saas, skybridge, codepilot, superpowers, gstack, ecc, claw-code, openmontage, cli-anything, deeptutor, aihelms, cc-haha, ai-website-cloner-template, ruview, medusa, appgenesisforge, weft, registry, a2ui-adk, cometchat-skills, pharaohfolio, posthog-superpower, andrej-karpathy-skills, open-generative-ai, tezgah.
- Multi-skill collections without a single distillable winner beyond what we took: orchestkit, agency-agents(-zh), ai-design-components, builder-skills, abu-cowork, agent-skills, skills (mattpocock), skills (anthropics — already mined), claude-skills (alirezarezvani — already mined; its business-ops/c-level/marketing sub-skills are off-stack for a dev library), skills-hub, skillnote, skilllens, lovcode, pm-skills, agentbro, maia-skill, editor-pro-max, carmack-council (51★ personal framework; orchestration covered by planning-multi-agent-work).
- Off-stack: blockchain vuln scanners (algorand/cairo/solana/substrate/ton), yara-rule-authoring, c-review, rust-review, qt/swift/kotlin-only material, claude-osint, anthropic-cybersecurity-skills (unofficial mirror repo, provenance concerns), interpreting-culture-index, genotoxic, graph-evolution, let-fate-decide, vibe-coding-rules, and remaining low-star (<20★) repos below the social floor.

### Notes / failure modes
- Medium + Anthropic RSS feeds returned 403 (blocked); two curated-list seed URLs 404. No X_BEARER_TOKEN / EXA_API_KEY, so X and web-search sources skipped.
- Heuristic uniqueness scoring (name/title/desc trigram) badly over-approves: 164 "creates" against an 82-skill library where nearly all were duplicates-by-territory, products, or lists. Consider adding a "repo is a skill, not a product/list" classifier signal (e.g. SKILL.md present at root, README/skill ratio).
