#!/usr/bin/env python3
"""Validate skills-database.json against the authoring rules.

Exits non-zero if:
  - Any skill is missing required fields.
  - `name` doesn't match ^[a-z0-9]+(?:-[a-z0-9]+)*$ or exceeds 64 chars.
  - `description` exceeds 1024 chars.
  - `description` + frontmatter_overrides.when_to_use exceeds 1536 chars (Claude's cap).
  - `skill_body` is shorter than 400 chars (shallow).
  - Any supporting file value is empty or stubby ("TODO", "starter", "add project-specific").
  - Two skills share the same `name`.

Separately warns if:
  - Any generated SKILL.md would exceed 500 lines (per docs Tip).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = json.loads((ROOT / "skills-database.json").read_text())

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
STUB_MARKERS = (
    "TODO",
    "starter support",
    "Add project-specific",
    "placeholder",
    "Lorem ipsum",
)

REQUIRED = {"name", "title", "category", "audience", "priority", "description", "trigger_phrases", "skill_body"}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    seen_names: set[str] = set()

    for i, s in enumerate(DB.get("skills", [])):
        missing = REQUIRED - set(s.keys())
        if missing:
            errors.append(f"skill[{i}] missing fields: {sorted(missing)}")
            continue

        name = s["name"]
        if name in seen_names:
            errors.append(f"duplicate name: {name}")
        seen_names.add(name)

        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{name}: invalid name (must match {NAME_RE.pattern}, <=64 chars)")

        if len(s["description"]) > 1024:
            errors.append(f"{name}: description >1024 chars ({len(s['description'])})")

        when = (s.get("frontmatter_overrides") or {}).get("when_to_use", "") or ""
        if len(s["description"]) + len(when) > 1536:
            errors.append(f"{name}: description + when_to_use >1536 chars")

        if len(s["skill_body"].strip()) < 400:
            errors.append(f"{name}: skill_body is shallow (<400 chars); add real content")

        if len(s.get("trigger_phrases", [])) < 3:
            errors.append(f"{name}: needs at least 3 trigger_phrases")

        for rel, content in (s.get("supporting_files") or {}).items():
            if not content or not content.strip():
                errors.append(f"{name}: supporting file '{rel}' is empty")
                continue
            if len(content.strip()) < 40:
                errors.append(f"{name}: supporting file '{rel}' is a stub (<40 chars)")
            if any(marker in content for marker in STUB_MARKERS):
                warnings.append(f"{name}: '{rel}' may contain a stub marker")

        # rough SKILL.md line check: frontmatter (~10) + body
        body_lines = s["skill_body"].count("\n") + 10
        if body_lines > 500:
            warnings.append(f"{name}: SKILL.md would be ~{body_lines} lines (soft cap 500)")

    for w in warnings:
        print(f"  warn: {w}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"OK: {len(seen_names)} skills validated ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
