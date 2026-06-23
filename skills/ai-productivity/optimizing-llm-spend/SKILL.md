---
name: optimizing-llm-spend
description: "Designs the LLM cost layer for Node and FastAPI services so AI features don't bleed margin: model routing, prompt caching, response streaming with early termination, request batching, and per-tenant budgets. Use when an AI endpoint is being scoped, when the monthly bill jumps, or when picking between Claude Haiku/Sonnet/Opus and OpenAI/Gemini for a workload."
when_to_use: Scoping a new LLM endpoint, debugging a sudden cost spike, or choosing between Anthropic, OpenAI, and Gemini for a specific workload.
---

## LLM Cost Architecture for Production Apps

Token cost is an architectural concern, not a billing line item. The decisions that matter (model choice, caching, streaming, request shape) are made when the endpoint is designed — retrofitting them after launch is 3x harder.

### When to Use

- Scoping a new AI endpoint in a FastAPI/Node service — model choice and prompt shape are about to be locked in
- Monthly Anthropic/OpenAI bill grew faster than usage and you need to find the leak
- A user-facing feature is too slow because Opus/GPT-5 was used where Haiku/4o-mini would have sufficed
- Multi-tenant app where one customer's usage shouldn't blow up shared margin

### When NOT to Use

- One-off internal tooling where dev time costs more than tokens — premature optimization
- A pure embeddings workload (RAG indexing) — different cost profile, see `building-rag-ready-docs`

### Decision Framework

1. **Route by complexity, not by default.** Cheap-first routing (Haiku/4o-mini handles → escalate to Sonnet/4o → escalate to Opus/o-series) cuts spend 60-80% on classification, extraction, and short summarization. Implement the router as middleware, not in each endpoint.
2. **Cache the prompt prefix.** Anthropic prompt caching and OpenAI response caching pay back within hours when system prompts are >1k tokens. Put cacheable content (system, tools, retrieved context) before per-request content.
3. **Stream and allow early termination.** A user who closes the tab at token 200 should stop generation. Wire `AbortController` (Node) or `asyncio.CancelledError` (FastAPI) through the SDK call.
4. **Batch async workloads.** Anthropic Message Batches API and OpenAI Batch API are 50% cheaper for non-interactive work (overnight summarization, embedding refreshes, daily classification).
5. **Set per-tenant budgets at the gateway.** Track tokens per `x-tenant-id` in Redis, hard-stop at the budget, soft-warn at 80%. Don't trust app code to enforce limits — race conditions will blow the cap.

### Anti-patterns

- Picking the most capable model and "optimizing later" — the prompts and prompts-of-prompts will be designed around it
- Logging full prompts/responses to your APM at INFO — that's a second cost line (storage, egress) and a PII liability
- Disabling caching during dev because "it's confusing" — your team forgets to re-enable it before launch
- Trusting client-side token counts — count server-side after the model returns; clients lie

### Worked Example — Express middleware router

```typescript
// chooseModel.ts
export function chooseModel(req: ChatRequest): ModelId {
  const tokens = estimateTokens(req.input);
  if (req.task === "classify" || req.task === "extract") return "claude-haiku-4-5";
  if (tokens < 4_000 && !req.requires_reasoning) return "claude-sonnet-4-6";
  return "claude-opus-4-6"; // long context + hard reasoning only
}
```

### Validation Loop

- [ ] Dashboard shows tokens-in/tokens-out by route, by model, by tenant
- [ ] Prompt caching hit-rate measured weekly (target >40% for system prompt tokens)
- [ ] Streaming endpoints abort generation on client disconnect (test with `curl --max-time`)
- [ ] Per-tenant budgets fire alerts at 80% and hard-stop at 100%
- [ ] Quarterly model audit: would Haiku handle this today? (often yes, after capability bumps)
