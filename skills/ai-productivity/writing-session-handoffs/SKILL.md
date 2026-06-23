---
name: writing-session-handoffs
description: Compacts a long Claude session into a handoff document the next agent (or your future self) can resume from cleanly. Use when ending a long pairing session, switching from research to implementation, splitting work across subagents, or when context is filling up and you need to checkpoint before the model loses the early decisions.
when_to_use: Ending a long session, switching modes (spec→build), or splitting work across parallel subagents.
---

## Session Handoffs Between Claude Agents

A handoff is not a chat transcript. It's the minimum context the next agent needs to make the same decisions you would, written so a fresh model session can pick up without re-deriving everything.

### When to Use

- Context window is past 60% and the early decisions matter more than the recent token churn
- Switching from research/spec mode to implementation mode (different mental model, different tools)
- Splitting work into parallel subagents that each need a slice of the context
- End of a long pairing session that will resume tomorrow or by a different teammate

### When NOT to Use

- The current session is short and the task is finishing — just finish it
- Pure exploration with no decisions yet to preserve — `/clear` is cheaper than a handoff

### Decision Framework

1. **State the goal in one sentence.** "Ship the FastAPI endpoint that returns paginated invoices for tenant X by Friday." Everything else hangs off this.
2. **List decisions made and the reasoning.** Not "we use Postgres" — "we use Postgres because the existing tenant DB is Postgres and adding another store would double the on-call surface." The reasoning is what the next agent needs to know whether to revisit.
3. **Capture open questions explicitly.** If the original session deferred a decision, name it as `OPEN:` so the next agent knows it's still in play.
4. **Pin the files that matter.** Absolute paths to the 3-10 files the next agent will read first. Don't list every file touched — list the entry points.
5. **Redact secrets before write.** API keys, tokens, customer data — strip them. Handoffs get committed, mailed, pasted into other tools.

### Anti-patterns

- Dumping the chat transcript verbatim — wastes the new context window on conversation overhead
- Skipping the open questions because they feel embarrassing — those are exactly what the next agent needs to know
- Writing the handoff to the project root — clutters the repo and risks committing secrets. Use `.handoff/` (gitignored) or `/tmp/`.
- Listing 200 files "for context" — the next agent reads 5. Pick the 5.

### Worked Example — handoff template

```markdown
# Handoff: invoices-pagination-endpoint
Date: 2026-05-25  Agent: Claude Opus 4.6

## Goal
Ship GET /api/invoices?tenant_id=&cursor= for the billing service by Fri 2026-05-29.

## Decisions made
- Cursor pagination, not offset (table is 8M rows, ORDER BY id DESC + WHERE id < cursor)
- Tenant isolation enforced in middleware (existing `require_tenant`), NOT re-checked in handler
- Response shape matches /api/orders for SDK consistency

## OPEN questions
- OPEN: do we expose `total_count`? Adds a second query — defer unless UX needs it
- OPEN: rate limit at 60 RPM per tenant or per API key? Asked product, no answer yet

## Entry-point files
- src/api/invoices.py — new handler goes here
- src/middleware/tenant.py — already does isolation, just use it
- tests/api/test_orders.py — copy as test scaffold

## Next concrete step
Write the handler signature + one happy-path test, then run pytest tests/api/test_invoices.py.
```

### Validation Loop

- [ ] Goal sentence is concrete and time-bound
- [ ] Every decision has a one-line "because…"
- [ ] Open questions are named, not buried
- [ ] File paths are absolute and exist
- [ ] No secrets present (grep `sk_`, `xoxb-`, `AKIA`, etc. before writing)
- [ ] Next concrete step is a single command or a single file edit
