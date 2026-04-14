---
name: hunter
description: Scours X, LinkedIn, Medium, and GitHub for high-quality Claude Code skills that fit a React/Next.js/TypeScript, Node.js, Python (FastAPI/Django), and Tailwind + shadcn stack. Merges findings into skills-database.json, honoring the library's dedup and overwrite rules. Use when the user says "run the hunter", "find new skills", "update the skills database", or when scheduled daily.
when_to_use: "Invoked by the daily GitHub Actions cron at 07:00 UTC, or manually via /hunter. Runs the full discover -> score -> merge -> commit pipeline."
disable-model-invocation: false
allowed-tools: "Bash(python *) Bash(gh *) Read Grep"
---

# Skills Hunter

Daily pipeline that discovers Claude Code skills on the public web, scores them, and folds the winners into this library without duplicating work.

## Execution contract

When invoked, run:

```
python hunter/run_hunter.py --stack react,nextjs,typescript,node,python,fastapi,django,tailwind,shadcn --mode auto-commit
```

The Python script owns the whole pipeline. This SKILL.md exists so a human (or Claude in an ad-hoc session) can trigger a run by typing `/hunter` and get the same result as the scheduled job.

## Pipeline stages

1. **Discover.** Pull candidate skills from the sources in `hunter/sources.yml`. For each source we capture: title, body, repo URL (if any), stars, forks, last-updated date, and the raw skill content when available.
2. **Score.** Rank every candidate against `hunter/quality_rubric.md`. Reject anything that is (a) off-stack, (b) below the star/fork floor, (c) stale (>12 months since last update on an unmaintained repo), or (d) already structurally identical to an existing skill.
3. **Decide.** For each winner:
   - **Create** a new skill if no entry in `skills-database.json` covers the same territory.
   - **Overwrite** an existing skill if the candidate is *materially better* (higher stars/forks, deeper body, more recent, or cleaner structure) AND occupies the same slot.
   - **Skip** if duplicate or worse.
4. **Merge.** Apply the create/overwrite decisions to `skills-database.json`, bump `version` and `generated_at`, and run `python tools/create_actual_skills.py` + `python scripts/generate_index.py` + `python scripts/validate_skills_db.py`.
5. **Commit.** If the validator passes AND there are real diffs, commit with message `hunter: +N new, ~M updated (YYYY-MM-DD)` and push.

## Management rules (enforced by the runner)

- **No duplicates.** Candidates are fuzzy-matched against existing `name`, `title`, and `trigger_phrases`. If overlap exceeds 0.80 cosine similarity the candidate is treated as an overwrite opportunity, not a new skill.
- **Overwrite only when better.** The runner computes a quality score (stars + forks + body depth + recency). An overwrite requires `new_score >= existing_score * 1.15`. Otherwise the existing skill wins.
- **Create when missing.** If similarity is below 0.60 AND the candidate passes the quality bar, it becomes a new skill.
- **Stack-relevance gate.** Any skill must match at least one of the stack tags passed via `--stack` OR sit in an always-on category (`security-reliability`, `ai-productivity`, `testing`).
- **Atomic commits.** One commit per run, with a rollup in the commit body listing every touched skill and why (created / overwritten / skipped).

## Supporting files

- [`run_hunter.py`](run_hunter.py) — the pipeline itself.
- [`sources.yml`](sources.yml) — curated list of source feeds and search queries.
- [`quality_rubric.md`](quality_rubric.md) — scoring criteria.
- [`CHANGELOG.md`](CHANGELOG.md) — append-only log of daily runs.

## Invocation examples

- Scheduled: GitHub Actions fires `.github/workflows/daily-hunter.yml` at 07:00 UTC.
- Manual (repo root): `python hunter/run_hunter.py --mode dry-run` to preview, then `--mode auto-commit` to apply.
- Manual (Claude): type `/hunter` from Claude Code inside this repo.

## Failure modes

- **API rate limits.** The runner caches responses under `hunter/.cache/` and backs off on 429.
- **ANTHROPIC_API_KEY missing.** Scoring uses a lightweight rubric pass; LLM-based body enrichment is skipped but a warning is logged.
- **Validator rejects the merge.** The run aborts before committing. The proposed diff lands in `hunter/.cache/last_rejected.json` for inspection.
