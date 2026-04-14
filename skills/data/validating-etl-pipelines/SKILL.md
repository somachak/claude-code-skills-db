---
name: validating-etl-pipelines
description: Validates ETL and ELT pipelines for freshness, schema drift, lineage breaks, duplication, and reconciliation errors. Use when building ingestion jobs, warehouse transforms, or sync systems.
---

# ETL Pipeline Validator

## When to Use This Skill

Use this skill when the task matches these patterns:

- etl validation
- schema drift
- pipeline freshness
- reconciliation
- warehouse

Use it for data, back-end workflows in the `data` category.

## What This Skill Does

Validates ETL and ELT pipelines for freshness, schema drift, lineage breaks, duplication, and reconciliation errors. Use when building ingestion jobs, warehouse transforms, or sync systems.

## Instructions

1. Read the relevant files, routes, modules, or configuration before making recommendations.
2. Identify the highest-risk decisions, edge cases, regressions, or architectural constraints first.
3. Apply the category-specific review and implementation notes in this skill.
4. Use the supporting files in this directory only when they are relevant to the task at hand.
5. Prefer minimal, verifiable changes over broad rewrites.
6. When the task changes behavior, recommend or produce a validation loop such as tests, checks, manual verification, or a review checklist.
7. If the task is high risk, summarize assumptions and failure modes before finalizing.

## Category-Specific Guidance

- Use machine-verifiable checks where possible and preserve sample failure diagnostics.

## Supporting Files

Recommended files to keep with this skill:

- `references/pipeline-checklist.md`
- `examples/data-reconciliation.md`
- `scripts/validate-pipeline.py`

## Build Guidance

- Keep SKILL.md concise and move larger detail into one-level-deep support files.
- Keep descriptions discoverable and written in third person.
- Prefer deterministic scripts for validation and repeatable checks.
- Evolve this skill through real usage and add examples only when they improve success on repeated tasks.

## Source Basis

This generated seed skill is based on the following references:

- https://code.claude.com/docs/en/skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://github.com/trailofbits/skills
- https://github.com/Aaronontheweb/dotnet-skills
- https://github.com/alirezarezvani/claude-skills
- https://github.com/slavingia/skills
- https://x.com/CodevolutionWeb/status/2034683638382506063
- https://x.com/JJEnglert/status/2038639244038521068
- https://x.com/ghumare64/status/2014246449593176406

