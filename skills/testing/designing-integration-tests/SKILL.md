---
name: designing-integration-tests
description: Designs integration tests around service contracts, persistence, side effects, and environment setup. Use when changes cross module, network, storage, or framework boundaries.
---

# Integration Test Designer

## When to Use This Skill

Use this skill when the task matches these patterns:

- integration test
- service contract
- testcontainers
- db integration
- api integration

Use it for back-end, full-stack workflows in the `testing` category.

## What This Skill Does

Designs integration tests around service contracts, persistence, side effects, and environment setup. Use when changes cross module, network, storage, or framework boundaries.

## Instructions

1. Read the relevant files, routes, modules, or configuration before making recommendations.
2. Identify the highest-risk decisions, edge cases, regressions, or architectural constraints first.
3. Apply the category-specific review and implementation notes in this skill.
4. Use the supporting files in this directory only when they are relevant to the task at hand.
5. Prefer minimal, verifiable changes over broad rewrites.
6. When the task changes behavior, recommend or produce a validation loop such as tests, checks, manual verification, or a review checklist.
7. If the task is high risk, summarize assumptions and failure modes before finalizing.

## Category-Specific Guidance

- Use realistic dependencies but keep setup repeatable and observable.

## Supporting Files

Recommended files to keep with this skill:

- `references/integration-test-guide.md`
- `examples/environment-fixtures.md`

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

