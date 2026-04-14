from pathlib import Path
import json
import shutil
import zipfile

base = Path('/home/user/workspace/claude-code-skills-db')
db = json.loads((base / 'skills-database.json').read_text())

skills_root = base / 'skills'
bundles_root = base / 'bundles'
if skills_root.exists():
    shutil.rmtree(skills_root)
if bundles_root.exists():
    shutil.rmtree(bundles_root)
skills_root.mkdir(parents=True, exist_ok=True)
bundles_root.mkdir(parents=True, exist_ok=True)

category_titles = {
    'frontend': 'Frontend Skills',
    'backend': 'Backend Skills',
    'data': 'Data Skills',
    'testing': 'Testing Skills',
    'platform': 'Platform Skills',
    'security-reliability': 'Security and Reliability Skills',
    'ai-productivity': 'AI Productivity Skills'
}

category_intro = {
    'frontend': 'Skills for UI architecture, accessibility, CSS systems, responsive behavior, bundle performance, and browser-facing security.',
    'backend': 'Skills for APIs, auth, jobs, services, concurrency, webhooks, event-driven systems, and backend documentation.',
    'data': 'Skills for schema design, SQL review, migrations, search/indexing, analytics instrumentation, and ETL validation.',
    'testing': 'Skills for unit, integration, E2E, snapshot, coverage, and production-bug regression workflows.',
    'platform': 'Skills for CI/CD, containers, infrastructure as code, monorepos, release workflows, and developer experience.',
    'security-reliability': 'Skills for threat modeling, secrets/config audits, observability, SLOs, failure modes, and recovery readiness.',
    'ai-productivity': 'Skills for extracting reusable skills, reviewing PRs, planning multi-agent work, building RAG-ready docs, and cataloging patterns.'
}

by_category = {}
for skill in db['skills']:
    by_category.setdefault(skill['category'], []).append(skill)


def md_bullets(items, code=False):
    if code:
        return '\n'.join(f'- `{item}`' for item in items)
    return '\n'.join(f'- {item}' for item in items)


def yaml_line(key, value):
    if isinstance(value, bool):
        return f'{key}: {'true' if value else 'false'}'
    text = str(value).replace('\n', ' ')
    if any(ch in text for ch in [':', '[', ']', '(', ')', '*', '"']):
        text = text.replace('"', '\\"')
        return f'{key}: "{text}"'
    return f'{key}: {text}'


def write_zip_from_directory(source_dir: Path, zip_path: Path, prefix: str):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(source_dir.rglob('*')):
            if p.is_file():
                zf.write(p, arcname=str(Path(prefix) / p.relative_to(source_dir)))


def render_skill(skill):
    frontmatter = {
        'name': skill['name'],
        'description': skill['description'],
    }
    frontmatter.update(skill.get('suggested_frontmatter', {}))

    lines = ['---']
    for k, v in frontmatter.items():
        lines.append(yaml_line(k, v))
    lines.extend([
        '---',
        '',
        f"# {skill['title']}",
        '',
        '## When to Use This Skill',
        '',
        'Use this skill when the task matches these patterns:',
        '',
        md_bullets(skill['trigger_phrases']),
        '',
        f"Use it for {', '.join(skill['audience'])} workflows in the `{skill['category']}` category.",
        '',
        '## What This Skill Does',
        '',
        skill['description'],
        '',
        '## Instructions',
        '',
        '1. Read the relevant files, routes, modules, or configuration before making recommendations.',
        '2. Identify the highest-risk decisions, edge cases, regressions, or architectural constraints first.',
        '3. Apply the category-specific review and implementation notes in this skill.',
        '4. Use the supporting files in this directory only when they are relevant to the task at hand.',
        '5. Prefer minimal, verifiable changes over broad rewrites.',
        '6. When the task changes behavior, recommend or produce a validation loop such as tests, checks, manual verification, or a review checklist.',
        '7. If the task is high risk, summarize assumptions and failure modes before finalizing.',
        '',
        '## Category-Specific Guidance',
        '',
        md_bullets(skill['implementation_notes']),
        '',
        '## Supporting Files',
        '',
        'Recommended files to keep with this skill:',
        '',
        md_bullets(skill['recommended_supporting_files'], code=True),
        '',
        '## Build Guidance',
        '',
        '- Keep SKILL.md concise and move larger detail into one-level-deep support files.',
        '- Keep descriptions discoverable and written in third person.',
        '- Prefer deterministic scripts for validation and repeatable checks.',
        '- Evolve this skill through real usage and add examples only when they improve success on repeated tasks.',
        '',
        '## Source Basis',
        '',
        'This generated seed skill is based on the following references:',
        '',
        md_bullets(skill['source_urls']),
        ''
    ])
    return '\n'.join(lines)

# root skills index
root_lines = [
    '# Skills Library',
    '',
    'This folder contains installable Claude Code skills grouped by category.',
    '',
    '## Categories',
    ''
]
for category in sorted(by_category):
    root_lines.append(f'- `{category}/` — {category_intro.get(category, "")}')
(skills_root / 'README.md').write_text('\n'.join(root_lines) + '\n')

for category, items in by_category.items():
    cat_dir = skills_root / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        f'# {category_titles.get(category, category.title())}',
        '',
        category_intro.get(category, ''),
        '',
        '## Included skills',
        ''
    ]
    for skill in sorted(items, key=lambda s: s['name']):
        lines.append(f'- `{skill["name"]}` — {skill["description"]}')
    (cat_dir / 'README.md').write_text('\n'.join(lines) + '\n')

    for skill in sorted(items, key=lambda s: s['name']):
        skill_dir = cat_dir / skill['name']
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / 'references').mkdir(parents=True, exist_ok=True)
        if any(p.startswith('scripts/') for p in skill['recommended_supporting_files']):
            (skill_dir / 'scripts').mkdir(parents=True, exist_ok=True)
        if any(p.startswith('templates/') for p in skill['recommended_supporting_files']):
            (skill_dir / 'templates').mkdir(parents=True, exist_ok=True)
        if any(p.startswith('examples/') for p in skill['recommended_supporting_files']):
            (skill_dir / 'examples').mkdir(parents=True, exist_ok=True)

        (skill_dir / 'SKILL.md').write_text(render_skill(skill) + '\n')

        for rel in skill['recommended_supporting_files']:
            p = skill_dir / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            title = Path(rel).stem.replace('-', ' ').replace('_', ' ').title()
            if rel.startswith('scripts/'):
                p.write_text('#!/usr/bin/env bash\n# Placeholder helper script for this skill. Replace with project-specific deterministic checks.\necho "Implement project-specific helper for this skill."\n')
                p.chmod(0o755)
            else:
                p.write_text(
                    f'# {title}\n\n'
                    f'This is a starter support file for `{skill["name"]}`.\n\n'
                    '## Purpose\n\n'
                    'Add project-specific guidance here to keep `SKILL.md` concise.\n\n'
                    '## Suggested content\n\n'
                    '- Decision rules\n'
                    '- Checklists\n'
                    '- Project conventions\n'
                    '- Examples\n'
                    '- Validator instructions\n'
                )

for category in sorted(by_category):
    cat_dir = skills_root / category
    write_zip_from_directory(cat_dir, bundles_root / f'{category}-skills.zip', category)

write_zip_from_directory(skills_root, bundles_root / 'all-skills.zip', 'skills')

sections = []
for category in sorted(by_category):
    sections.append(f'### {category_titles.get(category, category.title())}')
    sections.append('')
    sections.append(category_intro.get(category, ''))
    sections.append('')
    for skill in sorted(by_category[category], key=lambda s: s['name']):
        sections.append(f'- `{skill["name"]}` — {skill["description"]}')
    sections.append('')

readme = (
    '# Claude Code Skills DB\n\n'
    'A user-friendly, installable skill library for developers using Claude Code, backed by a source-based skills database and organized into real category folders with `SKILL.md` files.\n\n'
    '## Repo structure\n\n'
    '- `skills/` — installable skill folders grouped by category\n'
    '- `bundles/` — zip downloads for each category plus one full library bundle\n'
    '- `skills-database.json` — source-backed database used to generate the library\n'
    '- `skills-schema.json` — schema for the database\n'
    '- `daily-update-playbook.md` — guidance for recurring updates\n'
    '- `scripts/` — validation and Git sync helpers\n\n'
    '## How to use\n\n'
    '### Browse in GitHub\n\n'
    'Open the `skills/` folder and then choose a category such as `frontend`, `backend`, or `testing`.\n\n'
    '### Install manually\n\n'
    'Copy any skill folder into one of these Claude Code skill locations:\n\n'
    '- `~/.claude/skills/<skill-name>/SKILL.md` for personal use\n'
    '- `.claude/skills/<skill-name>/SKILL.md` for project use\n\n'
    'These locations and the `SKILL.md` entrypoint follow the official Claude Code skill structure [Claude Code Docs](https://code.claude.com/docs/en/skills).\n\n'
    '### Download bundles\n\n'
    'Use the zip files in `bundles/` if you want a grouped pack instead of copying one folder at a time.\n\n'
    '## Skill categories\n\n' + '\n'.join(sections) + '\n'
    '## Notes\n\n'
    'The repository uses official Claude Code skill guidance for skill structure, metadata, and discovery [Claude Code Docs](https://code.claude.com/docs/en/skills). The naming, description style, supporting-file structure, and iterative authoring approach are also aligned with Anthropic\'s best-practices guide [Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).\n'
)
(base / 'README.md').write_text(readme)

print(f'Generated {len(db["skills"])} skills across {len(by_category)} categories')
