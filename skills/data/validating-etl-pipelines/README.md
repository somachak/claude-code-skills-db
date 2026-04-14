# ETL Pipeline Validator — plain-English guide

## What this skill is for

Validates ETL and ELT pipelines for freshness, schema drift, lineage breaks, duplication, and reconciliation errors. Use when building ingestion jobs, warehouse transforms, or sync systems.

## In simple terms

This skill helps with etl pipeline validator work so you do not have to explain the same rules or workflow every time.

## When you would use it

- etl validation
- schema drift
- pipeline freshness
- reconciliation
- warehouse

## Example things you could ask for

- Use the validating-etl-pipelines skill to help with this task.
- Validates ETL and ELT pipelines for freshness, schema drift, lineage breaks, duplication, and reconciliation errors. Help me when building ingestion jobs, warehouse transforms, or sync systems.

## What the files mean

- `SKILL.md` is the main instruction file that Claude Code uses.
- `references/` contains background guidance or checklists.
- `examples/` contains example patterns or sample outputs.
- `templates/` contains starting templates you can adapt.
- `scripts/` contains helper scripts when the skill needs repeatable checks or automation.

## Jargon explained

- `etl` — Extract, transform, load. A process for moving and reshaping data from one system into another.
- `elt` — Extract, load, transform. Similar to ETL, but data is loaded first and transformed later, often in a data warehouse.
- `schema drift` — A change in the structure of incoming data that can break downstream logic.

## If you are unsure

Open `SKILL.md` only after reading this guide. If the words in `SKILL.md` feel too technical, use the example prompts above and keep your request in plain English.
