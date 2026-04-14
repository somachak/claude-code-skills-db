# Background Job Builder — plain-English guide

## What this skill is for

Designs reliable background jobs, retry logic, scheduling strategy, idempotency, and failure handling. Use when adding workers, task queues, cron-style jobs, or async processing pipelines.

## In simple terms

This skill helps with background job builder work so you do not have to explain the same rules or workflow every time.

## When you would use it

- queue worker
- retry logic
- idempotency
- scheduled job
- background task

## Example things you could ask for

- Use the building-background-jobs skill to help with this task.
- Designs reliable background jobs, retry logic, scheduling strategy, idempotency, and failure handling. Help me when adding workers, task queues, cron-style jobs, or async processing pipelines.

## What the files mean

- `SKILL.md` is the main instruction file that Claude Code uses.
- `references/` contains background guidance or checklists.
- `examples/` contains example patterns or sample outputs.
- `templates/` contains starting templates you can adapt.
- `scripts/` contains helper scripts when the skill needs repeatable checks or automation.

## Jargon explained

- `idempotency` — A property where repeating the same action does not create extra side effects or duplicate results.
- `observability` — The ability to understand what a system is doing by looking at logs, metrics, traces, and diagnostic signals.
- `cron` — A scheduled task that runs automatically at specific times.

## If you are unsure

Open `SKILL.md` only after reading this guide. If the words in `SKILL.md` feel too technical, use the example prompts above and keep your request in plain English.
