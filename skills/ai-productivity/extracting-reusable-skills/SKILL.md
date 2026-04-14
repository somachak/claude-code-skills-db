---
name: extracting-reusable-skills
description: Turns repeated successful workflows into reusable skills with proper names, descriptions, support files, and evaluation ideas. Use when recurring tasks reveal stable patterns worth codifying.
when_to_use: create a skill, extract workflow, reuse this process
---

## From Task to Reusable Skill

Repeated tasks should become reusable skills. The skill is recognizing when to extract, designing skill interfaces, and authoring clear, stack-specific documentation.

### When to Use

- Task is repeated across projects or team members
- Task is complex and domain-specific
- Pattern emerges in multiple codebases

### Decision Framework for Claude Code Skills

1. **Skill is self-contained and focused.** Not "do everything," but "generate SQL migration" or "audit component accessibility."
2. **Skill interface is clear.** Input (code snippet, requirements), output (generated artifact, audit report). Use Claude's first-class integration: read files, run commands, return markdown.
3. **Stack specificity.** Skill for React + TypeScript + Tailwind has different guidance than generic Vue. Reference specific patterns, libraries, tools.
4. **Skill body is 400-2500 chars.** Substantive, not boilerplate. Include "when to use," "decision framework," "anti-patterns," "checklist."
5. **Reference supporting files.** Complex checklists, examples, patterns → separate markdown files. Linked from skill body.

### Anti-patterns to Avoid

- Generic skill. "Help me code" + generic advice. Not useful.
- Bloated skill. 5000 chars of examples. Split into supporting files.
- No context. Skill doesn't mention React, Node, or databases. Sounds random.

### Checklist

- [ ] Skill solves a repeated problem (not one-off task)
- [ ] Skill is focused (one primary action, not many)
- [ ] Skill body is 400-2500 chars with decision framework and anti-patterns
- [ ] Skill references specific tech (React, FastAPI, Tailwind, etc.)
- [ ] Trigger phrases are natural (words engineers use)
- [ ] Supporting files are separate, linked from body
- [ ] Example usage is concrete (real code, not pseudocode)
- [ ] Skill is tested by running it on real codebase
