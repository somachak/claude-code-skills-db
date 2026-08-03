# AI Productivity Skills

Extracting reusable skills, reviewing PRs with Claude, planning multi-agent work, building RAG-ready docs, and cataloging patterns.

## Included skills

- [`asking-clarifying-questions/`](./asking-clarifying-questions/) — A 6-axis underspecification test paired with a 1–5 question template and a `defaults` fast-path.
- [`building-rag-ready-docs/`](./building-rag-ready-docs/) — Restructures documentation for retrieval quality with chunk-friendly sections, explicit metadata, and stable terminology.
- [`cataloging-codebase-patterns/`](./cataloging-codebase-patterns/) — Catalogs recurring codebase patterns, preferred implementations, and anti-patterns so future skills and prompts can reference real repository behavior.
- [`clarifying-underspecified-requests/`](./clarifying-underspecified-requests/) — Forces a structured clarification pass before any code is written when a request has multiple plausible interpretations — the most common cause of wasted Claude work in TS/React/Next and FastAPI/Django repos.
- [`claude-api/`](./claude-api/) — Build, debug, and optimize Claude API / Anthropic SDK apps.
- [`curating-team-conventions/`](./curating-team-conventions/) — Curates coding conventions, architectural defaults, and review standards into structured reference material that can later become skills.
- [`designing-deep-modules/`](./designing-deep-modules/) — Design modules with small interfaces and deep implementations using a precise shared vocabulary (module, interface, seam, adapter, depth).
- [`designing-workflow-skills/`](./designing-workflow-skills/) — Guides design and structuring of workflow-based Claude Code skills with multi-step phases, decision trees, subagent delegation, and progressive disclosure.
- [`evaluating-tooling-choices/`](./evaluating-tooling-choices/) — Evaluates libraries, frameworks, and platform choices using adoption fit, migration cost, risk, and operational burden.
- [`extracting-reusable-skills/`](./extracting-reusable-skills/) — Turns repeated successful workflows into reusable skills with proper names, descriptions, support files, and evaluation ideas.
- [`generating-pr-reviews/`](./generating-pr-reviews/) — Runs a four-phase pull request review (context, high-level, line-by-line, verdict) with severity-labeled feedback and stack-specific checkpoints for React/Next, TypeScript/Node, and Python/FastAPI/Django.
- [`optimizing-llm-spend/`](./optimizing-llm-spend/) — Designs the LLM cost layer for Node and FastAPI services so AI features don't bleed margin: model routing, prompt caching, response streaming with early termination, request batching, and per-tenant budgets.
- [`planning-multi-agent-work/`](./planning-multi-agent-work/) — Plans work decomposition, task boundaries, handoffs, and validation points for multi-agent development workflows.
- [`spec-driven-development/`](./spec-driven-development/) — Enforces writing a complete specification before any implementation begins.
- [`turning-runbooks-into-skills/`](./turning-runbooks-into-skills/) — Converts operational runbooks into reusable skills with standing instructions, validator loops, and safe invocation controls.
- [`writing-session-handoffs/`](./writing-session-handoffs/) — Compacts a long Claude session into a handoff document the next agent (or your future self) can resume from cleanly.
