# Claude Code Skills Database

A curated, daily-refreshed library of Claude Code skills for a **React / Next.js / TypeScript · Node.js · Python (FastAPI/Django) · Tailwind + shadcn/ui** stack.

Every skill follows the official authoring rules at <https://code.claude.com/docs/en/skills>: real domain content in `SKILL.md`, no generic boilerplate, supporting files only when they carry real content.

## What's in here

| Path | What it is |
|---|---|
| [`SKILLS_INDEX.md`](./SKILLS_INDEX.md) | Flat searchable index of every skill — generated, do not edit. |
| [`skills/`](./skills/) | 50 installable skills across 7 categories. Each folder has `SKILL.md` (what Claude reads) and `README.md` (what humans read). |
| [`bundles/`](./bundles/) | One zip per category plus `all-skills.zip` for bulk install. |
| [`skills-database.json`](./skills-database.json) | Source of truth. Every `SKILL.md` is rendered from here. |
| [`skills-schema.json`](./skills-schema.json) | JSON schema for the database. |
| [`tools/create_actual_skills.py`](./tools/create_actual_skills.py) | Generator. Renders `skills/` and `bundles/` from the database. |
| [`scripts/generate_index.py`](./scripts/generate_index.py) | Rebuilds `SKILLS_INDEX.md` from the database. |
| [`scripts/validate_skills_db.py`](./scripts/validate_skills_db.py) | Enforces authoring rules (naming, description caps, body depth, no-stub supporting files). |
| [`hunter/`](./hunter/) | The daily skills hunter — scours GitHub / Medium / X for new high-quality skills and merges the winners. |
| [`.github/workflows/daily-hunter.yml`](./.github/workflows/daily-hunter.yml) | Runs the hunter at **07:00 UTC every day** and commits its findings. |

## Install a skill

```bash
# Grab a specific skill
cp -R skills/frontend/building-accessible-ui ~/.claude/skills/

# Or grab a whole category
unzip bundles/frontend-skills.zip -d ~/.claude/skills/
```

## Local development loop

```bash
# edit skills-database.json
python tools/create_actual_skills.py   # regenerates skills/ + bundles/
python scripts/generate_index.py       # rebuilds SKILLS_INDEX.md
python scripts/validate_skills_db.py   # catches shallow bodies, naming issues, size caps
```

## The daily hunter

Every day at 07:00 UTC, `.github/workflows/daily-hunter.yml` runs `hunter/run_hunter.py` which:

1. Pulls candidate skills from curated GitHub repos, search queries, RSS feeds, and (if `X_BEARER_TOKEN` is set) X posts.
2. Scores each candidate against [`hunter/quality_rubric.md`](./hunter/quality_rubric.md) — stack fit, authoring compliance, social proof, depth, uniqueness.
3. Applies these rules:
   - **No duplicates.** Fuzzy-match against existing skill names, titles, triggers (>0.80 similarity = duplicate, skipped).
   - **Overwrite only when better.** A candidate must score ≥115% of the incumbent to replace it.
   - **Create when missing.** Low-similarity + high-score candidates become new skills.
4. Regenerates the library, validates, and commits with a rollup message like `hunter: +2 new, ~1 updated (YYYY-MM-DD)`.
5. Logs every decision — created, overwritten, skipped, rejected — to [`hunter/CHANGELOG.md`](./hunter/CHANGELOG.md).

Required repo secrets for the workflow: `ANTHROPIC_API_KEY` (optional but recommended), `EXA_API_KEY` (optional), `X_BEARER_TOKEN` (optional). `GITHUB_TOKEN` is provided automatically.

Trigger a manual run: **Actions → Daily Skills Hunter → Run workflow**. Or locally: `python hunter/run_hunter.py --mode dry-run`.

## Categories

- **frontend** — React / Next.js / TypeScript and Tailwind + shadcn UI patterns, accessibility, CSS architecture, responsive behavior, bundle performance, browser security.
- **backend** — Node.js, FastAPI, and Django patterns for APIs, auth, jobs, concurrency, webhooks, event-driven systems.
- **data** — Schema design, SQL review, migrations, search/indexing, analytics instrumentation, ETL validation.
- **testing** — Unit, integration, E2E, snapshot, coverage, production-bug regression.
- **platform** — CI/CD, containers, IaC, monorepos, release workflows, developer experience.
- **security-reliability** — Threat modeling, secrets audits, observability, SLOs, failure modes, recovery readiness.
- **ai-productivity** — Extracting reusable skills, reviewing PRs with Claude, planning multi-agent work, building RAG-ready docs, cataloging patterns.
