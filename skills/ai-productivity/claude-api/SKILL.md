---
name: claude-api
description: "Builds and debugs Claude API / Anthropic SDK applications: choosing between a single Messages call, a code-owned tool-use loop, and Managed Agents; current-generation defaults (adaptive thinking, effort levels, streaming, max_tokens sizing); prompt caching prefix discipline and silent-invalidator debugging; compaction vs context editing for long agent loops; task budgets vs max_tokens; and the migration breakages that return 400 (assistant prefills, budget_tokens, temperature/top_p). Use when writing or reviewing Anthropic SDK code, picking a model, debugging cache misses or truncated output, or migrating a codebase to a newer Claude model."
when_to_use: Use whenever code calls the Anthropic SDK or Claude API, when choosing a model or API surface, or when debugging caching, streaming, tool use, thinking config, or a model migration. Skip if the project targets a different LLM provider.
---

## Claude API & Anthropic SDK

Your training prior about model IDs, parameters, and pricing is stale by construction. Verify against `docs.claude.com` before writing model strings or quoting prices — this file is a decision map, not a price list.

### Defaults that are almost always right

- Model: `claude-opus-5`. Do not downgrade to Sonnet or Haiku for cost; that is the user's call, not yours.
- Thinking: `thinking: {type: "adaptive"}` for anything non-trivial. Adaptive lets the model decide depth per request.
- Streaming: on for any request with long input, long output, or high `max_tokens` — it is the fix for SDK HTTP timeouts. Use `.get_final_message()` / `.finalMessage()` when you don't need per-event handling.
- `max_tokens`: ~16000 non-streaming, ~64000 streaming. Lowballing truncates mid-thought and costs a full retry. Go small only for classification (~256) or deliberate short outputs.

**Use exact model ID strings with no date suffix.** `claude-sonnet-5`, not `claude-sonnet-5-20260114`. Date-suffixed variants you recall from training are a common source of 404s.

### Which surface?

| Need | Surface |
|---|---|
| Classify, summarize, extract, answer | Single Messages API call |
| Multi-step pipeline where *your code* owns the control flow | Messages API + tool use, loop in your code |
| Open-ended agent with your own tools and your own compute | Messages API + tool use (or the SDK's tool-runner helper) |
| Stateful agent with a hosted sandbox, file mounts, scheduling, versioned config | Managed Agents |

Start at the top and move down only when the task genuinely needs model-driven exploration. "Simplest" means the least code you own — for a scheduled or memory-backed agent, Managed Agents is usually simpler than hand-rolling a loop plus a scheduler plus state files.

Managed Agents flow is always **Agent (created once, versioned) → Session (per run)**. `model`, `system`, and `tools` live on the agent, never on the session. It is unsupported on Bedrock/Vertex/Foundry — use Messages API + tool use there.

### Prompt caching: the whole game is prefix stability

Render order is `tools` → `system` → `messages`. A single changed byte anywhere in the prefix invalidates everything after it.

```
[ tools (frozen, sorted) ][ system (frozen) ] ←cache_control  [ history ]  [ volatile: timestamp, user question ]
```

Put stable content first, volatile content after the last breakpoint. Max 4 breakpoints; minimum cacheable prefix ~1024 tokens — below that it silently doesn't cache.

**Verify, don't assume:** check `usage.cache_read_input_tokens` across repeated calls. Zero means a silent invalidator — `datetime.now()` in the system prompt, unsorted JSON keys, a tool list built from a set, or a per-request trace ID.

For operator instructions mid-conversation, append a `{"role": "system"}` message to `messages[]` rather than editing top-level `system`; editing `system` throws away the cached prefix. (Supported on the Opus/Fable tier, not Sonnet 5.)

### Long-running loops: compaction vs context editing

They are different features and easy to confuse.

- **Compaction** *summarizes* earlier context server-side as you approach the trigger threshold. Beta header `compact-2026-01-12`. **The critical mistake:** append the whole `response.content` back to `messages`, not just the extracted text — compaction blocks in the response are what the API uses to replace history on the next request. Extract only the string and you silently lose compaction state.
- **Context editing** *clears* old blocks rather than summarizing. On `client.beta.messages.*` with `context-management-2025-06-27`, pass `context_management={"edits": [{"type": "clear_tool_uses_20250919"}]}` (or `clear_thinking_20251015`). Cheapest fix when tool results, not reasoning, are the bloat.

### Task budgets ≠ max_tokens

`max_tokens` is a hard per-response ceiling the model cannot see; it gets cut off mid-sentence. A **task budget** is an advisory token ceiling for a whole agentic loop that the model *can* see, so it paces itself and lands the plane. Set `output_config={"effort": "high", "task_budget": {"type": "tokens", "total": 64000}}` on a streaming beta call (minimum total 20,000). Leave `remaining` unset — the server tracks the countdown; passing a client-computed `remaining` while also resending full history under-reports spend. Only set it when you rewrite history between requests.

### Migration pitfalls that bite

- **Assistant prefills are removed** on the current model generation and return 400. Use `output_config.format` (structured outputs) or a system-prompt instruction to control response shape.
- **`budget_tokens` is removed** on current models — `{type: "enabled", budget_tokens: N}` returns 400. Use `effort` levels instead.
- **Sampling params** (`temperature`, `top_p`, `top_k`) are rejected on current models.
- **Disabling thinking on Opus 5** is accepted only at effort `high` or below and degrades tool-call formatting. Prefer `effort: "low"` over disabling.
- **Never silently truncate** oversized input. Tell the user and offer chunking or summarization.
- **Confirm scope before a codebase migration.** "Migrate my project to Opus 5" names the what, not the where. Ask which directory or file list before editing.

### Pre-flight checklist

- [ ] Model ID verified against live docs, no date suffix appended
- [ ] `thinking: adaptive` set; no `budget_tokens`, no `temperature`
- [ ] Streaming enabled where output may be long
- [ ] `cache_read_input_tokens` observed non-zero on the second identical call
- [ ] Full `response.content` appended to history (not just text) if compaction is on
- [ ] Tool-use loop terminates on `stop_reason` and handles `max_tokens` as an error, not a result
