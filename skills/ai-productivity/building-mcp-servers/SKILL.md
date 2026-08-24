---
name: building-mcp-servers
description: "Designs and implements MCP (Model Context Protocol) servers in TypeScript (MCP SDK) or Python (FastMCP): tool granularity (coverage vs workflow tools), stdio vs stateless streamable-HTTP transport, Zod/Pydantic input schemas with outputSchema and structuredContent, the four tool annotations, pagination and response projection to protect the context window, actionable error messages, and a 10-question read-only evaluation set. Use when exposing an internal API or service to Claude as tools, reviewing an existing MCP server that agents use poorly, or deciding whether to ship one fat workflow tool or many primitives."
when_to_use: Use when building, reviewing, or debugging an MCP server in TypeScript or Python — tool design, transport choice, schemas, pagination, error text, or evals.
---

## Building MCP Servers

An MCP server is judged by one thing: can an agent complete a real task with it, first try, without burning the context window. Endpoint parity is not the goal — task completion is.

### Decision 1: Tool granularity

| Situation | Choose |
|---|---|
| Agent needs to compose arbitrary operations | Comprehensive endpoint coverage (`svc_list_x`, `svc_get_x`, `svc_create_x`) |
| One workflow dominates real usage (e.g. "triage a ticket") | A workflow tool that does the 4-call sequence server-side |
| Unsure | Default to coverage — composition is recoverable, a missing primitive is not |

The failure mode at each extreme: 200 thin CRUD tools blow the tool-definition budget before the first message; a single `do_everything(action, payload)` tool forces the model to guess an undocumented dispatch table.

### Decision 2: Transport

- **stdio** — local servers, desktop clients, anything reading the user's filesystem. No auth layer needed; the client owns the process.
- **Streamable HTTP, stateless JSON** — remote/hosted servers. Stateless means any replica can serve any request: no sticky sessions, trivial horizontal scaling. Reach for stateful sessions or SSE streaming only when you have a concrete need (long-running jobs with progress), because they turn a load-balancer config into a distributed-state problem.

### Decision 3: What comes back

Context is the scarce resource. Three rules:

1. **Never return the raw upstream JSON.** Project to the fields an agent can act on. A GitHub issue is `number, title, state, author, labels, url, body` — not 60 keys of `*_url` links.
2. **Paginate everything that can grow**, and return the cursor *in the response* with an explicit hint: `"next_cursor": "abc", "hint": "call again with cursor=abc for 30 more"`.
3. **Define `outputSchema` and return `structuredContent`** alongside the text block. Clients that support code execution can then filter results without round-tripping through the model.

### Worked example — TypeScript SDK

```ts
server.registerTool("linear_search_issues", {
  description: "Search Linear issues by text, team, and state. Returns up to 25 issues with a cursor for more.",
  inputSchema: {
    query: z.string().describe("Full-text search, e.g. 'login 500 error'"),
    teamKey: z.string().optional().describe("Team key like 'ENG'. Omit for all teams."),
    state: z.enum(["backlog","started","completed","canceled"]).optional(),
    cursor: z.string().optional(),
  },
  outputSchema: { issues: z.array(IssueSchema), nextCursor: z.string().nullable() },
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: true },
}, async ({ query, teamKey, state, cursor }) => {
  const page = await linear.search({ query, teamKey, state, after: cursor, first: 25 });
  const issues = page.nodes.map(toCompactIssue);
  return {
    content: [{ type: "text", text: renderMarkdownTable(issues) }],
    structuredContent: { issues, nextCursor: page.pageInfo.endCursor ?? null },
  };
});
```

Python/FastMCP is the same shape: `@mcp.tool` with Pydantic models for input and return type, docstring as the description.

### Annotations are not decoration

`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` are what let a client auto-approve safe calls and gate dangerous ones. Getting `destructiveHint: false` wrong on a delete tool is how an agent silently wipes a workspace. Set all four, deliberately, on every tool.

### Errors must be instructions

```
❌ "Error: 422 Unprocessable Entity"
✅ "teamKey 'ENGINEERING' not found. Valid keys: ENG, DES, OPS. Call linear_list_teams for the full list."
```

An error the agent can't act on costs a full retry loop. Include: what was wrong, what the valid values are, and which tool to call to discover them.

### Anti-patterns

- **Mirroring the REST API 1:1** including admin endpoints nobody will call. Ship the 10 tools that cover 90% of tasks.
- **Unbounded list responses.** One `list_all_records` on a real account returns 40k rows and ends the session.
- **Auth secrets in tool arguments.** Credentials come from env/config at server start, never from the model.
- **Swallowing failures** into `{"ok": false}` with no message.
- **Descriptions that repeat the tool name.** `"get_user: gets a user"` teaches nothing. Say what it returns, what the ID format is, and when to prefer it over the search tool.

### Evaluation before you ship

Write 10 questions, then verify you can answer each yourself using only the server. Each must be: independent, read-only, requiring 2+ tool calls, realistic, and stable (the answer won't change next month). Store as XML `<qa_pair><question>…</question><answer>…</answer></qa_pair>` and check answers by string comparison. If a question needs 6 tool calls where a human would need one lookup, that's the signal to add a workflow tool.

### Ship checklist

- [ ] Every tool has input constraints, a described output, and all four annotations
- [ ] Every list tool paginates and caps page size
- [ ] Error paths return actionable text, not status codes
- [ ] `npm run build` / `python -m py_compile` clean; verified in MCP Inspector
- [ ] 10 evals written and self-verified
- [ ] No credentials accepted as tool parameters
