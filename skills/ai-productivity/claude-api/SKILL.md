---
name: claude-api
description: "Build, debug, and optimize Claude API / Anthropic SDK apps. Always includes prompt caching. Handles migrating between Claude model versions and choosing between API surfaces (single call, tool use, agentic loop, Managed Agents). TRIGGER: code imports `anthropic`/`@anthropic-ai/sdk`; user asks for Claude API, Anthropic SDK, or Managed Agents; user adds/modifies a Claude feature (caching, thinking, tool use, batch, files, citations) or model. SKIP: file uses `openai`/other-provider SDK, provider-neutral code, general ML."
---

# Building LLM-Powered Applications with Claude

## Before You Start

Scan for non-Anthropic provider markers — `import openai`, `langchain_openai`, `OpenAI(`, `gpt-4`, filenames like `agent-openai.py` or `*-generic.py`. If found, ask whether to switch to Claude or keep non-Claude. Do not edit non-Anthropic files with Anthropic SDK calls.

**Never guess SDK usage.** Import paths, method signatures, and class names must come from explicit documentation. WebFetch the SDK repo rather than infer from another language.

## Defaults (non-negotiable)

- **Model**: `claude-opus-4-7` unless user explicitly names another. Do not downgrade for cost.
- **Thinking**: `thinking: {type: "adaptive"}` for anything remotely complex. `budget_tokens` is deprecated on 4.6/4.7.
- **Streaming**: Default for long input/output or high `max_tokens`. Use `.get_final_message()` if you don't need individual events.
- **Prompt caching**: Always include for large, repeated context.

## Which Surface to Use

| Use Case | Surface |
|----------|---------|
| Classification, summarization, extraction, Q&A | Claude API — single call |
| Multi-step with code-controlled logic | Claude API + tool use |
| Custom agent (you host compute + tools) | Claude API agentic loop |
| Server-managed stateful agent (Anthropic hosts execution) | Managed Agents |
| Third-party providers (Bedrock, Vertex, Foundry) | Claude API + tool use only — Managed Agents is 1P only |

**Decision tree:**
```
1. Is your deployment on Bedrock/Vertex/Foundry? → Claude API (Managed Agents unavailable)
2. Single LLM call? → Claude API
3. Want Anthropic to run agent loop + host container? → Managed Agents
4. Multi-step, you control the loop? → Claude API + tool use
5. Open-ended agent, you host compute? → Claude API agentic loop
```

**Should I build an agent?** Only if: (1) task is multi-step and hard to fully specify, (2) outcome justifies cost/latency, (3) Claude is capable at this task type, (4) errors can be caught and recovered from. "No" to any → stay simpler.

## Current Models (2026-04-15)

| Model | Model ID | Context | Input $/1M | Output $/1M |
|-------|----------|---------|------------|-------------|
| Claude Opus 4.7 | `claude-opus-4-7` | 1M | $5.00 | $25.00 |
| Claude Opus 4.6 | `claude-opus-4-6` | 1M | $5.00 | $25.00 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M | $3.00 | $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | $1.00 | $5.00 |

**CRITICAL**: Use exact model ID strings above. Do NOT append date suffixes. `claude-sonnet-4-5`, not `claude-sonnet-4-5-20250514`.

## Thinking & Effort

- **Opus 4.7**: `thinking: {type: "adaptive"}` only. `budget_tokens` is removed — 400 error if used. Default effort: `"xhigh"` is best for most tasks.
- **Opus 4.6 / Sonnet 4.6**: Use `thinking: {type: "adaptive"}`. `budget_tokens` deprecated but still functional as transitional escape hatch.
- **Effort**: `output_config: {effort: "low"|"medium"|"high"|"xhigh"|"max"}`. `max` Opus-only. `xhigh` Opus 4.7 only. Default is `high`.
- **Thinking display on Opus 4.7**: Thinking blocks stream empty by default. Set `thinking: {type: "adaptive", display: "summarized"}` to show visible progress.

## Language Detection

| File Pattern | SDK |
|-------------|-----|
| `*.py`, `pyproject.toml`, `requirements.txt` | Python (`anthropic`) |
| `*.ts`, `*.tsx`, `package.json` | TypeScript (`@anthropic-ai/sdk`) |
| `*.java`, `pom.xml`, `build.gradle` | Java |
| `*.go`, `go.mod` | Go |
| `*.rb`, `Gemfile` | Ruby |
| `*.cs`, `*.csproj` | C# |
| `*.php`, `composer.json` | PHP |

If multiple languages: check which the user's current file relates to. If ambiguous, ask.

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Use `requests`/`fetch` in Python/TS project | Use official SDK |
| Fall back to OpenAI-compatible shims | Use Anthropic SDK |
| Append date suffixes to model IDs | Use exact IDs from table |
| Use `budget_tokens` on new 4.6/4.7 code | Use `thinking: {type: "adaptive"}` |
| Choose model to save cost without asking user | Always use `claude-opus-4-7` as default |
| Infer API from another language's SDK | WebFetch the target language's SDK docs |

## Prompt Caching

Always include for large, repeated context (system prompts, long docs, tool definitions). Add `cache_control: {type: "ephemeral"}` to the last block of content you want cached. Cache TTL is 5 minutes (ephemeral). Saves cost significantly on repeated calls.

## Tool Use Pattern

```python
# Python — basic tool use loop
import anthropic

client = anthropic.Anthropic()

tools = [{"name": "get_weather", "description": "Get weather for a location", 
           "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}}]

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)
# Handle tool_use blocks in response.content
```

## Checklist

- [ ] Model ID is exact string from table (no date suffix appended)
- [ ] Using official Anthropic SDK for the project language, not requests/fetch
- [ ] Prompt caching added for large repeated context
- [ ] Streaming enabled for long requests
- [ ] Thinking set to `adaptive` (not `budget_tokens`) on 4.6/4.7
- [ ] Effort level appropriate for task (default `high`, use `xhigh` on Opus 4.7 for complex work)
