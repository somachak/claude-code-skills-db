# Hunter Changelog

Append-only log of every daily run. Every decision the hunter makes — create, overwrite, skip, reject — is logged here with its score so a human can audit the library's evolution after the fact.

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

