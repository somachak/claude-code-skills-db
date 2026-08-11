---
name: building-vercel-ai-sdk-agents
description: "Builds AI features and agents in TypeScript with the Vercel AI SDK v7: generateText/streamText, structured output via Output.object, ToolLoopAgent for in-memory tool loops, WorkflowAgent for durable resumable runs, runtimeContext/toolsContext separation, toolApproval for sensitive tools, and v6-to-v7 breaking changes (instructions vs system, isStepCount, aggregated usage, finalStep). Use when adding LLM features to a Next.js/Node app or migrating AI SDK major versions."
when_to_use: Use when implementing LLM features or agents in a TypeScript/Node/Next.js app with the Vercel AI SDK, choosing between ToolLoopAgent and WorkflowAgent, wiring tool approvals, or migrating v6 code to v7.
---

## Vercel AI SDK v7: Agents and Core Functions

First step, always: confirm the installed major version (`node_modules/ai/package.json`) before writing code - v6 and v7 APIs differ in breaking ways, and AI SDK APIs move too fast to trust memory. v7 requires Node >= 22 and is ESM-only.

### Choosing an Agent Architecture

- **`ToolLoopAgent` (from `ai`)** - ordinary app-server agents where losing in-memory state on restart is acceptable. Exposes `generate()`/`stream()`.
- **`WorkflowAgent` (from `@ai-sdk/workflow`)** - runs that must survive process restarts, deploys, interrupted streams, or delayed human approval. Stream-first (`stream()` only); durable tools are marked `'use step'`; state must stay serializable.
- **`HarnessAgent` (from `@ai-sdk/harness/agent`)** - wraps an external agent runtime (Claude Code, Codex) with sandboxing. Experimental; keep adapter code easy to swap.

### Core v7 Patterns

```ts
import { generateText, isStepCount, Output } from 'ai';
import { z } from 'zod';

const result = await generateText({
  model,                       // resolve from project config; never hard-code from memory
  instructions: 'Answer concisely.',   // NOT `system` (deprecated in v7)
  prompt: 'Classify this ticket.',
  stopWhen: isStepCount(3),            // renamed from stepCountIs
  timeout: { totalMs: 60_000, stepMs: 15_000 },
  output: Output.object({ schema: z.object({ priority: z.enum(['low','medium','high']) }) }),
});
result.output;              // structured result - never JSON.parse(result.text)
```

### Context: Two Channels, Different Jobs

`runtimeContext` carries loop-wide state (tenant ID, feature flags, request ID) and reaches `prepareStep`, callbacks, and telemetry. `toolsContext` carries per-tool secrets/config: each tool declares a `contextSchema` and receives only its own validated `context` in `execute`. Anything the model must reason about goes in messages or `instructions` instead - context is invisible to the model.

### Tool Approvals

Any tool that mutates data, spends money, runs commands, or reads private data gets a `toolApproval` entry (`'user-approval'`, or a function inspecting parsed input and context that returns approved/denied/user-approval). When the browser controls chat history, sign approvals with `experimental_toolApprovalSecret` so they are HMAC-verified server-side before execution. Workflow agents use tool-level `needsApproval` instead.

### v6 -> v7 Migration Traps

- `system` -> top-level `instructions`; system messages inside `messages` are rejected by default.
- `experimental_output` -> `output`; read `result.output`.
- `result.usage` (and `toolCalls`, `content`, etc.) now aggregate **all** steps; use `result.finalStep.usage` for the old behavior. For `streamText`, await `result.finalStep` first.
- `fullStream` -> `stream`; `onChunk` receives all part types, so guard on `part.type`.
- Lifecycle renames: `onFinish` -> `onEnd`, `onStepFinish` -> `onStepEnd`, `experimental_telemetry` -> `telemetry`.
- Result helper methods are deprecated: use stateless `toUIMessageStream` + `createUIMessageStreamResponse`.

### Checklist

- Installed `ai` major version verified; ESM imports throughout.
- Structured output uses `Output.object`, not manual JSON parsing.
- Every loop has `stopWhen` and a `timeout`; long-latency tools get per-tool `toolMs` overrides.
- Sensitive tools gated by approvals; secrets flow through `toolsContext`, never interpolated into prompts.
- Durable flows use `WorkflowAgent` with serializable context; resume state persisted from `detach()`/`stop()`, not by replaying UI history.
- Type safety: export `InferAgentUIMessage<typeof agent>` for typed useChat integration.
