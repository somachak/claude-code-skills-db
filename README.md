
# Claude Code Developer Skills Database

This database is designed to become a long-lived source of truth for developer-oriented skills that are valuable in Claude Code workflows.

It is intentionally structured around official Claude Code skill rules first, then public repository patterns, then community best practices. The goal is not to collect random prompts. The goal is to curate reusable, discoverable skills that can be turned into real `SKILL.md` directories with predictable quality.

## What is included

- A structured JSON database of seed skills for front-end, back-end, data, testing, platform, security, and AI-assisted development work.
- A schema file to keep the data consistent as it grows.
- A validation script that checks basic naming and description rules.
- A daily update playbook for recurring maintenance.

## Source-backed design principles

Official Claude Code docs state that each skill should live in its own directory with `SKILL.md` as the required entrypoint and can include supporting files like templates, examples, and scripts [Claude Code Docs](https://code.claude.com/docs/en/skills).

The same documentation explains that discovery depends heavily on metadata, especially the description, and that skills can be invoked directly or automatically when relevant [Claude Code Docs](https://code.claude.com/docs/en/skills).

Anthropic's skill authoring guidance recommends concise names, third-person descriptions that say what the skill does and when to use it, and keeping `SKILL.md` short while moving larger references into supporting files [Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

The authoring guide also recommends evaluation-driven development, validator loops, and avoiding deep reference chains, which is why this database stores supporting-file suggestions and implementation notes for each entry [Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

Large public repositories show that high-value libraries tend to cluster skills by domain, provide plugin-style packaging, and use clear naming schemes instead of one giant undifferentiated collection [Trail of Bits skills](https://github.com/trailofbits/skills), [Aaron Stannard's dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills), [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), [slavingia/skills](https://github.com/slavingia/skills).

Community posts on X repeatedly emphasize lean context, strong feedback loops, test-and-verify behavior, and small high-signal skill sets rather than bloated libraries, which supports maintaining this database as a curated set instead of a raw dump [CodevolutionWeb on X](https://x.com/CodevolutionWeb/status/2034683638382506063), [JJ Englert on X](https://x.com/JJEnglert/status/2038639244038521068), [ghumare64 on X](https://x.com/ghumare64/status/2014246449593176406).

## How to turn an entry into a real skill

1. Pick one database entry from `skills-database.json`.
2. Create a folder named after the `name` field.
3. Create `SKILL.md` with YAML frontmatter.
4. Copy the `description` into the frontmatter and adapt the suggested fields under `suggested_frontmatter`.
5. Create the support files listed in `recommended_supporting_files` only if the skill genuinely needs them.
6. Keep instructions concise and promote long references into separate files.
7. Add evaluation scenarios before expanding the skill.

## Recommended build order

Start with these high-leverage skills first:

- building-accessible-ui
- designing-rest-apis
- planning-data-migrations
- stabilizing-e2e-tests
- hardening-ci-pipelines
- threat-modeling-features
- extracting-reusable-skills

## Files

- `skills-database.json` — the structured database
- `skills-schema.json` — JSON schema for the database
- `daily-update-playbook.md` — repeatable update instructions
- `scripts/validate_skills_db.py` — validation helper
