---
name: generating-pr-reviews
description: Runs a four-phase pull request review (context, high-level, line-by-line, verdict) with severity-labeled feedback and stack-specific checkpoints for React/Next, TypeScript/Node, and Python/FastAPI/Django. Use when reviewing PRs, self-reviewing before merge, establishing team review standards, or mentoring reviewers.
when_to_use: pr review, code review, diff review, self-review before merge, setting review standards
---

## Structured Pull Request Review

Review is a quality gate and a teaching channel. The failure mode is unstructured skimming: the reviewer burns attention on naming while an auth bypass sails through. Fix it with a phased pass, explicit severity labels, and a hard line between what humans review and what tooling catches.

### Phase 1 — Context (2–3 min)
- Read the PR description and linked issue. No description? Ask for one before reading code.
- Check size: over ~400 changed lines, request a split. Review quality collapses past that.
- Confirm CI is green. Never line-review a red build.
- Note migrations, feature flags, or config changes — these drive the risk level of everything else.

### Phase 2 — High-level (5–10 min)
- Does the shape of the solution fit the problem? Wrong-layer fixes (patching a symptom in the UI when the bug is in the API contract) are the most expensive thing to catch late.
- Scan for architectural smells: new cross-module imports, duplicated logic, a "utils" dumping ground growing.
- Check the test diff first: what edge cases did the author think about? Missing tests for the risky path is a finding in itself.

### Phase 3 — Line-by-line (10–20 min)
Stack-specific checkpoints:
- **React/Next**: effects that should be derived state or events; missing dependency-array entries; server/client component boundary leaks (secrets or heavy deps imported into client components); unstable props causing re-renders; uncancelled async in effects.
- **TypeScript/Node**: `any` laundering through casts; floating promises (missing `await`/`.catch`); error paths that swallow context; input parsed without a schema (zod/valibot) at the boundary.
- **Python/FastAPI/Django**: mutable default arguments; blocking calls inside `async def`; N+1 queries (missing `select_related`/`selectin` loading); Pydantic models trusted past the boundary they validated.
- **Everywhere**: injection via string-built queries/commands; authz checked on the happy path only (IDOR); secrets in diffs; TOCTOU between check and use.
- **Reuse audit**: before accepting new helper code, grep for an existing utility that already does it. Duplicate helpers are how codebases rot.

### Phase 4 — Verdict (2–3 min)
Summarize top concerns, name one thing done well, then decide: approve / comment / request changes. "Approve once you add a test for X" beats an open-ended "request changes."

### Severity labels — use them on every comment
- `[blocking]` must fix before merge (bugs, security, data loss)
- `[important]` should fix; discuss if you disagree
- `[nit]` optional polish, never blocks
- `[suggestion]` alternative approach to consider
- `[learning]` context for the author, no action
- `[praise]` call out good work explicitly

### Feedback technique
- Ask, don't assert: "What happens if `items` is empty?" lands better than "this breaks on empty input" — and sometimes you're wrong.
- Suggest, don't command: "Would extracting this shared logic make sense? It appears in 3 places."
- Critique code, never the author. Prioritize: two `[blocking]` comments beat fifteen nits.

### Do not review manually
Formatting, import order, lint violations, typos. If these reach human review, fix the CI pipeline — that's the actionable finding.

### Anti-patterns
- Nit storms that bury the one real issue.
- Reviewing 2,000-line PRs in one sitting — approve-fatigue guarantees misses.
- Sitting on reviews >24h: context evaporates and conflicts pile up.
- Restating personal preference as a defect. If the style guide doesn't say it, it's a `[suggestion]`.

### Checklist
- [ ] CI green, PR under ~400 lines (or split requested)
- [ ] Tests cover the risky path, not just the happy path
- [ ] Error handling present; no swallowed exceptions or floating promises
- [ ] Authz + input validation checked at every new boundary
- [ ] No N+1s, no blocking calls in async contexts
- [ ] Reuse audit done — no duplicate helpers introduced
- [ ] Every comment labeled with severity; verdict explicit
