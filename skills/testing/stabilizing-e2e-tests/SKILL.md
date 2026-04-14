---
name: stabilizing-e2e-tests
description: Improves end-to-end tests by removing flakiness, clarifying waits, and aligning assertions with user-visible outcomes. Use when browser tests are brittle or slow.
---

# E2E Test Stabilizer

## When to Use This Skill

Use this skill when the task matches these patterns:

- playwright flake
- cypress flake
- e2e instability
- retrying tests
- waiting for ui

Use it for front-end, full-stack, qa workflows in the `testing` category.

## What This Skill Does

Improves end-to-end tests by removing flakiness, clarifying waits, and aligning assertions with user-visible outcomes. Use when browser tests are brittle or slow.

## Instructions

1. Read the relevant files, routes, modules, or configuration before making recommendations.
2. Identify the highest-risk decisions, edge cases, regressions, or architectural constraints first.
3. Apply the category-specific review and implementation notes in this skill.
4. Use the supporting files in this directory only when they are relevant to the task at hand.
5. Prefer minimal, verifiable changes over broad rewrites.
6. When the task changes behavior, recommend or produce a validation loop such as tests, checks, manual verification, or a review checklist.
7. If the task is high risk, summarize assumptions and failure modes before finalizing.

## Category-Specific Guidance

- Lean on deterministic selectors, network awareness, and state setup shortcuts.

## Supporting Files

Recommended files to keep with this skill:

- `references/e2e-stability-guide.md`
- `examples/flaky-patterns.md`

## Build Guidance

- Keep SKILL.md concise and move larger detail into one-level-deep support files.
- Keep descriptions discoverable and written in third person.
- Prefer deterministic scripts for validation and repeatable checks.
- Evolve this skill through real usage and add examples only when they improve success on repeated tasks.

## Source Basis

This generated seed skill is based on the following references:

- https://code.claude.com/docs/en/skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://github.com/trailofbits/skills
- https://github.com/Aaronontheweb/dotnet-skills
- https://github.com/alirezarezvani/claude-skills
- https://github.com/slavingia/skills
- https://x.com/CodevolutionWeb/status/2034683638382506063
- https://x.com/JJEnglert/status/2038639244038521068
- https://x.com/ghumare64/status/2014246449593176406

