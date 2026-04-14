---
name: generating-pr-reviews
description: Reviews pull requests for correctness, risk, test gaps, migration impact, and maintainability. Use when preparing PR feedback, self-reviewing changes, or training reviewers.
when_to_use: pr review, code review, diff review
---

## Systematic Code Review

Code review is knowledge transfer and quality gate. The skill is reviewing efficiently, catching real issues (not style), and providing actionable feedback.

### When to Use

- Every PR (before merge)
- Code review becomes time-consuming
- Need to scale review across team

### Decision Framework for Code Review

1. **Automate style; review substance.** Linter catches style. Reviewer focuses on logic, performance, security.
2. **Review checklist is explicit.** Does code change have tests? Is error handling present? Are edge cases covered? Use checklist to stay consistent.
3. **Comment is actionable.** Not "bad variable name." "Variable `x` is unclear; use `paymentAmount` instead."
4. **Approve with conditions.** "Approve once you add test for edge case X" is clearer than "request changes" without hope of resolution.
5. **Review is timely.** PR waiting 3 days for review = slow merge, merge conflicts. Target 24-hour reviews.

### Anti-patterns to Avoid

- Nitpicky review. Style issues that linter should catch. Wastes time.
- No structure. Review comments are random. Reviewer missed security issue because distracted by naming.
- Slow reviews. PR sits for days; context is lost.

### Checklist

- [ ] Linter passes (code style is automated)
- [ ] Tests are included (unit, integration, or E2E)
- [ ] Error handling is present (no silent failures)
- [ ] Security considerations (auth, input validation, no secrets)
- [ ] Performance is reasonable (no N+1 queries, no memory leaks)
- [ ] Documentation is updated (code comments, README)
- [ ] Commit messages are clear (not "WIP" or "fix stuff")
- [ ] Edge cases are handled (null, empty, boundary conditions)
- [ ] PR is under 400 lines (reviewable in <30min)
