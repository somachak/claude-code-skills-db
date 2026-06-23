# Clarifying Underspecified Requests Before Implementing

**Category:** ai-productivity · **Priority:** core · **Audience:** full-stack

Forces a structured clarification pass before any code is written when a request has multiple plausible interpretations — the most common cause of wasted Claude work in TS/React/Next and FastAPI/Django repos. Use when scope, acceptance criteria, target framework version, data shape, or rollback plan are unclear. Pushes the agent to ask 1-5 must-have questions with multiple-choice answers and a `defaults` shortcut, then restate the requirements before starting. SKIP when the request is already concrete or a 30-second discovery read can answer the open questions.

## When Claude should reach for this

Trigger phrases: `clarify requirements`, `ask questions first`, `underspecified`, `ambiguous request`, `before implementing`, `scope unclear`, `acceptance criteria`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
