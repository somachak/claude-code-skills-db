# Daily Claude Code Skills Database Update Task

Read these files first:

- /home/user/workspace/claude-code-skills-db/skills-database.json
- /home/user/workspace/claude-code-skills-db/skills-schema.json
- /home/user/workspace/claude-code-skills-db/daily-update-playbook.md
- /home/user/workspace/claude-code-skills-db/README.md

Task:

Update /home/user/workspace/claude-code-skills-db/skills-database.json using the official Claude Code skills docs, Anthropic's skill authoring best practices, public GitHub repositories, general web sources, and public X discussions.

Goals:

- Keep the database highly valuable for developers using Claude Code, especially front-end and back-end developers.
- Keep categories balanced across frontend, backend, data, testing, platform, security-reliability, and ai-productivity.
- Add new skill entries only when the pattern is reusable, clearly source-backed, and aligned with official skill-creation rules.
- Refine existing entries when a clearer or more discoverable description is supported by the sources.
- Ensure every skill entry includes a concrete description of what the skill does and when to use it.
- Prefer concise, discoverable names and third-person descriptions.
- Preserve the JSON schema shape.

Source priority:

1. https://code.claude.com/docs/en/skills
2. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
3. Relevant public GitHub skill repositories and public repository discussions
4. Public web pages and public X discussions with specific, repeatable insights

Validation:

Run:
python /home/user/workspace/claude-code-skills-db/scripts/validate_skills_db.py

If validation fails, fix the file before finishing.

Finish condition:

- Database remains valid
- Timestamp and version are refreshed if changes were made
- No speculative or weakly supported entries are added
