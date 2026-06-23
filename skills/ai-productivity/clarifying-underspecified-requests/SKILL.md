---
name: clarifying-underspecified-requests
description: "Forces a structured clarification pass before any code is written when a request has multiple plausible interpretations — the most common cause of wasted Claude work in TS/React/Next and FastAPI/Django repos. Use when scope, acceptance criteria, target framework version, data shape, or rollback plan are unclear. Pushes the agent to ask 1-5 must-have questions with multiple-choice answers and a `defaults` shortcut, then restate the requirements before starting. SKIP when the request is already concrete or a 30-second discovery read can answer the open questions."
when_to_use: Use whenever a request has multiple plausible interpretations or scope/acceptance/version/rollback details are missing. Skip when the request is already concrete or a 30-second config read answers the open questions.
---

# Clarifying Underspecified Requests

The single biggest source of wasted agent work is implementing the wrong thing confidently. This skill is the gate: before code, before commands, before a long plan, decide whether the request is specified well enough to act on. If not, ask the smallest set of questions that eliminate whole branches of wrong work.

## Decide: is this underspecified?

Treat the request as underspecified if any of these are unclear after a quick read:

- **Objective** — what changes vs stays the same
- **Done** — acceptance criteria, examples, edge cases
- **Scope** — which files / components / users / endpoints are in or out
- **Constraints** — framework version (Next.js 14 vs 15 vs 16, Pydantic v1 vs v2, Django 4 vs 5), perf budget, style guide, dependency limits
- **Environment** — runtime, package manager, build/test runner, deployment target
- **Safety** — data migration, rollout/rollback, blast radius

If two reasonable engineers would build different things, it's underspecified.

## Don't ask what you can quickly read

Cheap discovery beats clarifying questions. Before asking, do these in seconds:

- `package.json` / `pyproject.toml` for framework + version
- `tsconfig.json` `target`, `strict`, `paths`
- `next.config.js` for App vs Pages router signal
- Existing test file for the convention (vitest? pytest? jest?)
- A representative neighbour file for the style

If discovery answers a question, do not ask it.

## Ask 1-5 must-have questions

Optimize the questions for low friction:

- Numbered, short — not paragraphs
- Multiple choice with sensible defaults marked **bold**
- Include a "Not sure — use default" option
- Provide a `defaults` shortcut so the user can reply with one word
- Compact decision format — user can answer `1b 2a 3default`

### Template

```text
Before I start, I need:

1) Scope?
   a) **Just the bug fix in `src/api/auth.ts`** (default)
   b) Refactor the whole auth module while I'm in there
   c) Not sure — use default

2) Compatibility?
   a) **Stay on Next.js 15** (default)
   b) Bump to 16 as part of this change
   c) Not sure — use default

3) Tests?
   a) **Add a Vitest case for the regression** (default)
   b) Skip tests for now
   c) Not sure — use default

Reply with `defaults` to accept all, or e.g. `1a 2b 3a`.
```

## Pause until answers arrive

Until must-have answers come back:

- **Don't** run shell commands that mutate state, edit files, or write a long plan that depends on the unknowns.
- **Do** allow yourself a clearly labeled, low-risk discovery read — inspecting repo structure, opening config, reading the relevant function. State that this is discovery, not commitment.

If the user explicitly says "just go" without answering:

1. State assumptions as a numbered list ("I'll assume Next.js 15 stays, scope is `src/api/auth.ts` only, add a Vitest regression test").
2. Ask one final confirmation.
3. Proceed only after `yes` / corrections.

## Confirm interpretation, then build

Once answers arrive, restate the requirements in 1-3 sentences. Include the answers chosen and the success criterion. Then start work.

Example: *"Got it: fix the cookie-domain bug in `src/api/auth.ts` only, stay on Next.js 15, add a Vitest case that fails on the current code and passes after the fix. Starting now."*

## Anti-patterns

| Don't | Do Instead |
|---|---|
| Open with "I'll start by ..." on an ambiguous request | Run the underspecified gate first |
| Ask 8 paragraph-length questions | Ask 1-5 numbered, multiple-choice, with defaults |
| Ask things you could read from `package.json` in 2 seconds | Discover first, ask only what's truly unknown |
| Proceed silently with assumptions when blocked | State assumptions, ask one confirmation, then proceed |
| Treat user pushback ("just do it") as a license to skip restating | Always restate the interpretation before writing code |
| Lock the conversation — the user can't bypass questions | Always provide a `defaults` shortcut and a "Not sure" option |

## Checklist

- [ ] Read the request twice; listed missing dimensions explicitly
- [ ] Did the cheap discovery pass (configs, neighbour files) before asking
- [ ] Asked ≤ 5 questions, all multiple-choice with defaults
- [ ] Offered `defaults` shortcut and "Not sure" option
- [ ] No state-mutating commands run while waiting for answers
- [ ] Restated requirements in 1-3 sentences after answers arrived
