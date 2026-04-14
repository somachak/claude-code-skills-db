
# Daily Update Playbook

Use this playbook to update the developer skills database in a disciplined way.

## Objective

Keep `skills-database.json` current and valuable for developers using Claude Code, with equal attention to front-end and back-end work plus supporting areas such as testing, platform, security, data, and AI-assisted engineering.

## Source priority

1. Official Claude Code skills docs: https://code.claude.com/docs/en/skills
2. Anthropic skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
3. Public GitHub repositories with meaningful skill libraries and active structure
4. Public community tips and patterns from the web and X when they are concrete and repeatable

## Update workflow

1. Read `skills-database.json`, `skills-schema.json`, and this playbook.
2. Re-check the official docs for any format or discovery changes.
3. Review public GitHub repositories that publish Claude Code skills or closely related developer skill libraries.
4. Review public web and X discussions for concrete new techniques, patterns, or category gaps.
5. Add new skill entries only when they are clearly reusable and valuable beyond a single project.
6. Update existing descriptions when a better, more discoverable wording is supported by the documentation or repeated community usage.
7. Keep names lowercase and hyphenated, descriptions in third person, and support-file suggestions one level deep.
8. Run `python /home/user/workspace/claude-code-skills-db/scripts/validate_skills_db.py`.
9. If validation fails, fix the database before ending the run.
10. Update version and generated timestamp if the file changed.

## Inclusion rules

Add a skill only if all conditions are met:

- The workflow appears reusable across teams or codebases.
- The skill can be described clearly in one paragraph.
- The value is meaningful for developers, not generic productivity fluff.
- The skill fits one of the defined categories or justifies a new category.
- There is at least one strong supporting source and preferably more than one.

## Exclusion rules

Do not add entries that are:

- Thin wrappers around a single tool command with no durable workflow value
- One-off personal habits with no broader reuse
- Vague ideas like `coding-helper` or `frontend-tools`
- Names that contain reserved words such as `claude` or `anthropic`

## Output rules

For every new or edited entry, preserve:

- `name`
- `title`
- `category`
- `audience`
- `priority`
- `description`
- `trigger_phrases`
- `recommended_supporting_files`
- `implementation_notes`
- `suggested_frontmatter`
- `source_urls`

## Suggested recurring task instruction

Update `/home/user/workspace/claude-code-skills-db/skills-database.json` using the official Claude Code skills docs, public GitHub repositories, the web, and public X discussions. Keep the database highly valuable for front-end and back-end developers. Add or refine entries only when the pattern is reusable, clearly source-backed, and aligned to official skill-creation rules. Ensure every skill entry includes a concrete description of what the skill does and when to use it. Run the validator before finishing.
