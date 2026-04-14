# Snapshot Regression Checks — plain-English guide

## What this skill is for

Applies snapshot and golden-file testing carefully for stable outputs such as APIs, emails, rendered templates, and serialization. Use when outputs should remain consistent over time.

## In simple terms

This skill helps with snapshot regression checks work so you do not have to explain the same rules or workflow every time.

## When you would use it

- snapshot testing
- golden file
- approval testing
- email snapshot

## Example things you could ask for

- Use the snapshot-regression-checks skill to help with this task.
- Applies snapshot and golden-file testing carefully for stable outputs such as APIs, emails, rendered templates, and serialization. Help me when outputs should remain consistent over time.

## What the files mean

- `SKILL.md` is the main instruction file that Claude Code uses.
- `references/` contains background guidance or checklists.
- `examples/` contains example patterns or sample outputs.
- `templates/` contains starting templates you can adapt.
- `scripts/` contains helper scripts when the skill needs repeatable checks or automation.

## Jargon explained

- `golden file` — A saved expected output used to detect unwanted changes later.
- `approval testing` — A testing style where current output is compared to an approved expected output.
- `snapshot testing` — A testing approach that saves expected output and alerts you if it changes later.

## If you are unsure

Open `SKILL.md` only after reading this guide. If the words in `SKILL.md` feel too technical, use the example prompts above and keep your request in plain English.
