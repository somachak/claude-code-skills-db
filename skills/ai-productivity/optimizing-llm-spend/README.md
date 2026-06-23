# LLM Cost Architecture for Production Apps

**Category:** ai-productivity · **Priority:** supporting · **Audience:** back-end, full-stack

Designs the LLM cost layer for Node and FastAPI services so AI features don't bleed margin: model routing, prompt caching, response streaming with early termination, request batching, and per-tenant budgets. Use when an AI endpoint is being scoped, when the monthly bill jumps, or when picking between Claude Haiku/Sonnet/Opus and OpenAI/Gemini for a workload.

## When Claude should reach for this

Trigger phrases: `llm cost`, `token optimization`, `prompt caching`, `model routing`, `ai spend`, `anthropic vs openai cost`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
