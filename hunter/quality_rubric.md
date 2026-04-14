# Skill Quality Rubric

Every candidate gets scored on five dimensions. Total score is the weighted sum. The hunter rejects candidates below **60/100**, and only *overwrites* an existing skill if the candidate scores at least **15% higher**.

## 1. Stack fit (weight 25)

- **25** — Explicitly targets React / Next / TS, Node, Python (FastAPI/Django), or Tailwind/shadcn.
- **15** — Stack-agnostic but immediately applicable (e.g. API design, accessibility, testing strategy).
- **5**  — Tangential but useful (e.g. dev-loop tips, AI-productivity patterns).
- **0**  — Off-stack (mobile-only, game dev, data science pipelines without backend relevance). **Reject.**

## 2. Authoring-rule compliance (weight 25)

Checks the raw SKILL.md against https://code.claude.com/docs/en/skills:

- Frontmatter present with `description`.
- `description` front-loads the use case and fits under 1,536 chars with `when_to_use`.
- Body contains real decision-making content (checklists, anti-patterns, worked examples) — not generic instructions Claude already knows.
- Body stays under 500 lines.
- Supporting files (if any) carry real content, not stubs.

Score 5 per passing criterion (max 25). Anything scoring below 15 is **rejected** regardless of popularity.

## 3. Social proof / maintenance (weight 20)

For GitHub-sourced candidates:

- **20** — ≥500 stars, ≥50 forks, commit in last 90 days.
- **15** — ≥100 stars, ≥15 forks, commit in last 180 days.
- **10** — ≥20 stars, ≥5 forks, commit in last 365 days.
- **5**  — Below the thresholds but author has other high-signal repos.
- **0**  — Abandoned or low-signal. **Reject unless body quality is exceptional (≥22 on dimension 2).**

For X / blog candidates:

- **20** — Post has ≥200 likes or ≥50 reposts, author is verified or has ≥10k followers.
- **10** — Engagement visible but modest.
- **0**  — No visible signal.

## 4. Depth (weight 20)

- **20** — Includes: decision framework, anti-patterns section, at least one worked example, and a checklist or validation loop.
- **12** — Three of the four above.
- **6**  — Two of the four.
- **0**  — One or zero. **Reject.**

## 5. Uniqueness (weight 10)

Fuzzy similarity (trigram + cosine) against existing skills in `skills-database.json`:

- **10** — Similarity <0.40 (clearly net-new territory).
- **6**  — Similarity 0.40–0.60 (adjacent to existing skill; consider as supporting file instead).
- **3**  — Similarity 0.60–0.80 (overwrite candidate — must beat incumbent by 15%).
- **0**  — Similarity >0.80 (duplicate). **Skip.**

## Final decision

```
total = stack_fit + compliance + social + depth + uniqueness

if total < 60:               reject
elif uniqueness >= 6:        CREATE new skill
elif uniqueness >= 3:
    if total >= existing.total * 1.15:  OVERWRITE
    else:                               skip
else:                        skip  # duplicate
```

Every decision (accepted, overwritten, rejected, skipped) is appended to `hunter/CHANGELOG.md` with its score breakdown so a human can audit after the fact.
