---
name: asking-clarifying-questions
description: "A 6-axis underspecification test paired with a 1–5 question template and a `defaults` fast-path. Use before a Next.js migration, FastAPI/Django endpoint change, schema migration, or any work that touches user data. Complements `clarifying-underspecified-requests` with stack-specific hot spots (RSC boundary, pydantic v1/v2, Tailwind tokens, Postgres online migration)."
when_to_use: Ambiguous request, multiple plausible interpretations, scope/criteria unclear, touches data/auth/migrations, or version/runtime unknown.
---

## Asking Clarifying Questions Before You Code

Most failed sessions are failures of interpretation, not execution. Run the 6-axis test before editing any file; ask the smallest set of questions that eliminates whole branches of wrong work.

### The 6-Axis Underspecification Test

1. **Objective** — what should change vs. stay the same.
2. **Done** — acceptance criteria, examples, edge cases.
3. **Scope** — which files, routes, components, users are in/out.
4. **Constraints** — compatibility, performance, dependency budget.
5. **Environment** — Node/Python versions, framework version (Next 14 vs 15? FastAPI 0.110 vs 0.115?), package manager.
6. **Safety** — data migration, rollout, rollback, blast radius.

Two or more fuzzy axes → underspecified.

### Question Template (1–5 only)

```text
1) Scope?
   a) Just `/app/(auth)/login`
   b) All routes under `/app/(auth)/`
   c) Every place we read the session  **(default)**

2) Behaviour on existing rows?
   a) Backfill with default  **(default)**
   b) Leave NULL; gate at app layer
   c) Refuse migration if any NULLs

Reply `defaults` or e.g. `1c 2a`.
```

### Stack-Specific Hot Spots

- **Next.js**: server vs. client boundary, app router vs. pages router, RSC caching strategy.
- **FastAPI / Django**: sync vs. async, pydantic v1 vs v2, ORM session lifecycle.
- **Tailwind / shadcn**: arbitrary values vs. tokens, dark-mode strategy.
- **Postgres**: online migration with default vs. NOT NULL; index build CONCURRENTLY.

### Anti-Patterns

- Wall-of-paragraph questions. Bullets and numbered options always win.
- More than 5 questions — ship a short PRD instead.
- Long "discovery" reads that silently commit you to a direction.
- Proceeding on unstated assumptions when the user says "just go".

### Checklist

- [ ] All six axes have a concrete answer.
- [ ] Questions are numbered, multiple-choice, with a default.
- [ ] Included a one-word fast-path (`defaults`).
- [ ] Restated the goal before opening any file for edit.
