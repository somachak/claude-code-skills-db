# Claude API & Anthropic SDK Development

**Category:** ai-productivity · **Priority:** supporting · **Audience:** full-stack, backend

Builds and debugs Claude API / Anthropic SDK applications: choosing between a single Messages call, a code-owned tool-use loop, and Managed Agents; current-generation defaults (adaptive thinking, effort levels, streaming, max_tokens sizing); prompt caching prefix discipline and silent-invalidator debugging; compaction vs context editing for long agent loops; task budgets vs max_tokens; and the migration breakages that return 400 (assistant prefills, budget_tokens, temperature/top_p). Use when writing or reviewing Anthropic SDK code, picking a model, debugging cache misses or truncated output, or migrating a codebase to a newer Claude model.

## When Claude should reach for this

Trigger phrases: `claude api`, `anthropic sdk`, `prompt caching`, `tool use loop`, `model migration`, `managed agents`, `context editing`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
