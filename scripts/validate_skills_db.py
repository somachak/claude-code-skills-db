
from pathlib import Path
import json
import re
import sys

path = Path('/home/user/workspace/claude-code-skills-db/skills-database.json')
obj = json.loads(path.read_text())
errors = []
seen = set()

for i, skill in enumerate(obj.get('skills', []), start=1):
    name = skill.get('name', '')
    desc = skill.get('description', '')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        errors.append(f'{i}: invalid name format: {name}')
    if len(name) > 64:
        errors.append(f'{i}: name too long: {name}')
    if 'claude' in name or 'anthropic' in name:
        errors.append(f'{i}: reserved word in name: {name}')
    if name in seen:
        errors.append(f'{i}: duplicate name: {name}')
    seen.add(name)
    if not desc or len(desc) > 1024:
        errors.append(f'{i}: invalid description length for {name}')
    lowered = desc.lower().strip()
    if lowered.startswith('i ') or lowered.startswith('i can') or lowered.startswith('you ') or lowered.startswith('use me'):
        errors.append(f'{i}: description should be third person for {name}')
    if 'use when' not in lowered:
        errors.append(f'{i}: description should include when-to-use guidance for {name}')

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)

print(f'VALIDATION PASSED: {len(obj.get("skills", []))} skills checked')
