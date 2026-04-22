# Differential Security Review

**Category:** security-reliability · **Priority:** supporting · **Audience:** full-stack, backend

Security-focused differential review of code changes (PRs, commits, diffs). Adapts analysis depth to codebase size, uses git history for context, calculates blast radius, checks test coverage, and generates comprehensive markdown reports. Automatically detects security regressions. Risk-first: focuses on auth, crypto, value transfer, external calls.

## When Claude should reach for this

Trigger phrases: `differential review`, `security review pr`, `code diff security`, `blast radius`, `security regression`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
