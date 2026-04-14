from pathlib import Path
import json

base = Path('/home/user/workspace/claude-code-skills-db')
db = json.loads((base / 'skills-database.json').read_text())
skills_root = base / 'skills'

jargon = {
    'runbook': 'A step-by-step operating guide for doing a task safely and consistently, especially for operational or release work.',
    'idempotency': 'A property where repeating the same action does not create extra side effects or duplicate results.',
    'pagination': 'Splitting large result sets into smaller pages so they can be loaded and browsed safely.',
    'hydration': 'The process where browser JavaScript takes over a server-rendered page and makes it interactive.',
    'rbac': 'Role-based access control, meaning permissions are assigned based on roles such as admin or editor.',
    'slo': 'Service level objective, a target for reliability or performance such as uptime or response speed.',
    'sli': 'Service level indicator, the measurement used to evaluate whether the service is meeting its objective.',
    'etl': 'Extract, transform, load. A process for moving and reshaping data from one system into another.',
    'elt': 'Extract, load, transform. Similar to ETL, but data is loaded first and transformed later, often in a data warehouse.',
    'schema drift': 'A change in the structure of incoming data that can break downstream logic.',
    'outbox pattern': 'A way to store database changes and outgoing events together so they stay consistent.',
    'federation': 'A way to combine multiple GraphQL services into one larger graph.',
    'resolver': 'The code that fetches or computes a field in a GraphQL API.',
    'stale closure': 'A bug where code keeps using an old value because it captured earlier state.',
    'design token': 'A reusable named design value like a color, spacing size, or font style.',
    'vector search': 'A way to search using meaning or similarity rather than only exact keywords.',
    'tracking plan': 'A structured list of analytics events and properties that should be recorded in a product.',
    'golden file': 'A saved expected output used to detect unwanted changes later.',
    'approval testing': 'A testing style where current output is compared to an approved expected output.',
    'threat model': 'A structured way to think through what could go wrong, who could abuse a feature, and how to reduce that risk.',
    'observability': 'The ability to understand what a system is doing by looking at logs, metrics, traces, and diagnostic signals.',
    'monorepo': 'A single repository that contains multiple apps, packages, or services together.',
    'iac': 'Infrastructure as code, meaning cloud or infrastructure setup is defined in code files.',
    'rag': 'Retrieval-augmented generation, where an AI system looks up relevant documents before answering.',
    'e2e': 'End-to-end. A test that checks a full user flow from start to finish.',
    'snapshot testing': 'A testing approach that saves expected output and alerts you if it changes later.',
    'webhook': 'A message sent automatically from one system to another when an event happens.',
    'cicd': 'Continuous integration and continuous delivery, meaning code is automatically tested and prepared or deployed through pipelines.',
    'cron': 'A scheduled task that runs automatically at specific times.'
}

example_prompts = {
    'building-accessible-ui': [
        'Review this form UI for accessibility issues and tell me what to fix first.',
        'Check whether this modal and keyboard flow would be usable for screen reader and keyboard-only users.'
    ],
    'designing-rest-apis': [
        'Design a clean REST API for products, orders, and returns.',
        'Review this endpoint design and suggest a better pagination and error response pattern.'
    ],
    'turning-runbooks-into-skills': [
        'Turn this deployment checklist into a reusable Claude Code skill.',
        'Convert this operational guide into a skill folder with a clear SKILL.md and supporting files.'
    ]
}

def find_terms(text):
    found = []
    lower = text.lower()
    for term, meaning in jargon.items():
        if term in lower:
            found.append((term, meaning))
    return found

for skill in db['skills']:
    skill_dir = skills_root / skill['category'] / skill['name']
    if not skill_dir.exists():
        continue

    text_blob = ' '.join([
        skill['title'],
        skill['description'],
        ' '.join(skill['trigger_phrases']),
        ' '.join(skill['implementation_notes']),
        ' '.join(skill['recommended_supporting_files'])
    ])
    found = find_terms(text_blob)

    prompts = example_prompts.get(skill['name'], [
        f"Use the {skill['name']} skill to help with this task.",
        skill['description'].replace('Use when', 'Help me when')
    ])

    lines = [
        f"# {skill['title']} — plain-English guide",
        '',
        '## What this skill is for',
        '',
        skill['description'],
        '',
        '## In simple terms',
        '',
        f"This skill helps with {skill['title'].lower()} work so you do not have to explain the same rules or workflow every time.",
        '',
        '## When you would use it',
        '',
    ]
    for trig in skill['trigger_phrases'][:6]:
        lines.append(f'- {trig}')
    lines += [
        '',
        '## Example things you could ask for',
        ''
    ]
    for p in prompts:
        lines.append(f'- {p}')

    lines += [
        '',
        '## What the files mean',
        '',
        '- `SKILL.md` is the main instruction file that Claude Code uses.',
        '- `references/` contains background guidance or checklists.',
        '- `examples/` contains example patterns or sample outputs.',
        '- `templates/` contains starting templates you can adapt.',
        '- `scripts/` contains helper scripts when the skill needs repeatable checks or automation.',
    ]

    if found:
        lines += [
            '',
            '## Jargon explained',
            ''
        ]
        seen = set()
        for term, meaning in found:
            if term in seen:
                continue
            seen.add(term)
            lines.append(f'- `{term}` — {meaning}')

    lines += [
        '',
        '## If you are unsure',
        '',
        'Open `SKILL.md` only after reading this guide. If the words in `SKILL.md` feel too technical, use the example prompts above and keep your request in plain English.',
        ''
    ]

    (skill_dir / 'README.md').write_text('\n'.join(lines))

print('Generated plain-English README.md files for all skills')
