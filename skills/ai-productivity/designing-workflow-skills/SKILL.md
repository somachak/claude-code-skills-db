---
name: designing-workflow-skills
description: Guides design and structuring of workflow-based Claude Code skills with multi-step phases, decision trees, subagent delegation, and progressive disclosure. Use when creating skills with sequential pipelines, routing patterns, safety gates, task tracking, phased execution, or any multi-step workflow. Also applies when reviewing or refactoring existing workflow skills for quality.
---

# Designing Workflow Skills

Build workflow-based skills that execute reliably by following structural patterns, not prose.

## Essential Principles

<essential_principles>

<principle name="description-is-the-trigger">
**The `description` field is the only thing that controls when a skill activates.**

Claude decides whether to load a skill based solely on its frontmatter `description`. The body of SKILL.md — including "When to Use" and "When NOT to Use" sections — is only read AFTER the skill is already active. Put your trigger keywords, use cases, and exclusions in the description. A bad description means wrong activations or missed activations regardless of what the body says.

"When to Use" and "When NOT to Use" sections still serve a purpose: they scope the LLM's behavior once active. "When NOT to Use" should name specific alternatives: "use Semgrep for simple pattern matching" not "not for simple tasks."
</principle>

<principle name="numbered-phases">
**Phases must be numbered with entry and exit criteria.**

Unnumbered prose instructions produce unreliable execution order. Every phase needs:
- A number (Phase 1, Phase 2, ...)
- Entry criteria (what must be true before starting)
- Numbered actions (what to do)
- Exit criteria (how to know it's done)
</principle>

<principle name="tools-match-executor">
**Tools must match the executor.**

Skills use `allowed-tools:` in frontmatter. Agents use `tools:` in frontmatter. Subagents get tools from their `subagent_type`. Never list tools the component doesn't use. Never use Bash for operations that have dedicated tools (Glob, Grep, Read, Write, Edit).

Most skills and agents should include `TodoRead` and `TodoWrite` in their tool list — these enable progress tracking during multi-step execution and are useful even for skills that don't explicitly manage tasks.
</principle>

<principle name="progressive-disclosure">
**Progressive disclosure is structural, not optional.**

SKILL.md stays under 500 lines. It contains only what the LLM needs for every invocation: principles, routing, quick references, and links. Detailed patterns go in `references/`. Step-by-step processes go in `workflows/`. One level deep — no reference chains.
</principle>

<principle name="scalable-tool-patterns">
**Instructions must produce tool-calling patterns that scale.**

Every workflow instruction becomes tool calls at runtime. If a workflow searches N files for M patterns, combine into one regex — not N×M calls. If a workflow spawns subagents per item, use batching — not one subagent per file. Apply the 10,000-file test: mentally run the workflow against a large repo and check that tool call count stays bounded. See [anti-patterns.md](references/anti-patterns.md) AP-18 and AP-19.
</principle>

<principle name="degrees-of-freedom">
**Match instruction specificity to task fragility.**

Not every step needs the same level of prescription. Calibrate per step:
- **Low freedom** (exact commands, no variation): Fragile operations — database migrations, crypto, destructive actions. "Run exactly this script."
- **Medium freedom** (pseudocode with parameters): Preferred patterns where variation is acceptable. "Use this template and customize as needed."
- **High freedom** (heuristics and judgment): Variable tasks — code review, exploration, documentation. "Analyze the structure and suggest improvements."

A skill can mix freedom levels. A security audit skill might use high freedom for the discovery phase ("explore the codebase for auth patterns") and low freedom for the reporting phase ("use exactly this severity classification table").
</principle>

</essential_principles>

## When to Use

- Designing a new skill with multi-step workflows or phased execution
- Creating a skill that routes between multiple independent tasks
- Building a skill with safety gates (destructive actions requiring confirmation)
- Structuring a skill that uses subagents or task tracking
- Reviewing or refactoring an existing workflow skill for quality
- Deciding how to split content between SKILL.md, references/, and workflows/

## When NOT to Use

- Simple single-purpose skills with no workflow (just guidance) — write the SKILL.md directly
- Writing the actual domain content of a skill (this teaches structure, not domain expertise)
- Plugin configuration (plugin.json, hooks, commands) — use plugin development guides
- Non-skill Claude Code development — this is specifically for skill architecture

## Pattern Selection

Choose the right pattern for your skill's structure. Read the full pattern description in [workflow-patterns.md](references/workflow-patterns.md).

```
How many distinct paths does the skill have?
|
+-- One path, always the same
|   +-- Does it perform destructive actions?
|       +-- YES -> Safety Gate Pattern
|       +-- NO  -> Linear Progression Pattern
|
+-- Multiple independent paths from shared setup
|   +-- Routing Pattern
|
+-- Multiple dependent steps in sequence
    +-- Do steps have complex dependencies?
        +-- YES -> Task-Driven Pattern
        +-- NO  -> Sequential Pipeline Pattern
```

### Pattern Summary

| Pattern | Use When | Key Feature |
|---------|----------|-------------|
| **Routing** | Multiple independent tasks from shared intake | Routing table maps intent to workflow files |
| **Sequential Pipeline** | Dependent steps, each feeding the next | Auto-detection may resume from partial progress |
| **Linear Progression** | Single path, same every time | Numbered phases with entry/exit criteria |
| **Safety Gate** | Destructive/irreversible actions | Two confirmation gates before execution |
| **Task-Driven** | Complex dependencies, partial failure tolerance | TaskCreate/TaskUpdate with dependency tracking |

## Structural Anatomy

Every workflow skill needs this skeleton, regardless of pattern:

```markdown
---
name: kebab-case-name
description: "Third-person description with trigger keywords — this is how Claude decides to activate the skill"
allowed-tools:
  - [minimum tools needed]
# Optional fields — see tool-assignment-guide.md for full reference:
# disable-model-invocation: true    # Only user can invoke (not Claude)
# user-invocable: false             # Only Claude can invoke (hidden from / menu)
# context: fork                     # Run in isolated subagent context
# agent: Explore                    # Subagent type (requires context: fork)
# model: [model-name]               # Switch model when skill is active
# argument-hint: "[filename]"       # Hint shown during autocomplete
---

# Title

## Essential Principles
[3-5 non-negotiable rules with WHY explanations]

## When to Use
[4-6 specific scenarios — scopes behavior after activation]

## When NOT to Use
[3-5 scenarios with named alternatives — scopes behavior after activation]

## [Pattern-Specific Section]
[Routing table / Pipeline steps / Phase list / Gates]

## Quick Reference
[Compact tables for frequently-needed info]

## Reference Index
[Links to all supporting files]

## Success Criteria
[Checklist for output validation]
```

Skills support three types of string substitutions: dollar-prefixed variables for arguments and session ID, and exclamation-backtick syntax for shell preprocessing. The skill loader processes these before Claude sees the file — even inside code fences — so never use the raw syntax in documentation text. See [tool-assignment-guide.md](references/tool-assignment-guide.md) for the full variable reference and usage guidance.

> *Full skill: see source_url*
