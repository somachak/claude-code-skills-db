#!/usr/bin/env python3
"""
Generate installable Claude Code skills from skills-database.json.

This generator follows the official authoring rules at
https://code.claude.com/docs/en/skills:

  - SKILL.md = YAML frontmatter + real domain content only.
  - No generic "Instructions" boilerplate Claude already knows.
  - No "What This Skill Does" section that restates the description.
  - No build metadata, no source URL lists in SKILL.md.
  - Supporting files carry real content, never stubs.
  - SKILL.md stays under 500 lines; detail lives in supporting files.

Schema contract (skills-database.json skills[i]):

  required:
    name, title, category, audience, priority, description,
    trigger_phrases, skill_body

  optional:
    frontmatter_overrides   -> extra YAML frontmatter fields
    supporting_files        -> { "references/foo.md": "# real content..." }
    legacy_notes            -> carried forward for hunter diffs, not rendered
"""

from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "skills-database.json"
SKILLS_ROOT = ROOT / "skills"
BUNDLES_ROOT = ROOT / "bundles"

CATEGORY_TITLES = {
    "frontend": "Frontend Skills",
    "backend": "Backend Skills",
    "data": "Data Skills",
    "testing": "Testing Skills",
    "platform": "Platform Skills",
    "security-reliability": "Security and Reliability Skills",
    "ai-productivity": "AI Productivity Skills",
}

CATEGORY_INTRO = {
    "frontend": "React / Next.js / TypeScript and Tailwind + shadcn UI patterns, accessibility, CSS architecture, responsive behavior, bundle performance, and browser-facing security.",
    "backend": "Node.js, FastAPI, and Django patterns for APIs, auth, jobs, concurrency, webhooks, event-driven systems, and backend documentation.",
    "data": "Schema design, SQL review, migrations, search/indexing, analytics instrumentation, and ETL validation.",
    "testing": "Unit, integration, E2E, snapshot, coverage, and production-bug regression workflows.",
    "platform": "CI/CD, containers, infrastructure as code, monorepos, release workflows, and developer experience.",
    "security-reliability": "Threat modeling, secrets/config audits, observability, SLOs, failure modes, and recovery readiness.",
    "ai-productivity": "Extracting reusable skills, reviewing PRs with Claude, planning multi-agent work, building RAG-ready docs, and cataloging patterns.",
}


def yaml_scalar(value: Any) -> str:
    """Emit a YAML scalar. Quote if the value contains YAML-significant chars."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(yaml_scalar(v) for v in value) + "]"
    text = str(value).replace("\n", " ").strip()
    needs_quote = any(c in text for c in ":#&*?|>!%@`") or text.startswith("-") or text in {"true", "false", "null", "yes", "no"}
    if needs_quote:
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def render_frontmatter(skill: Dict[str, Any]) -> str:
    fields: Dict[str, Any] = {
        "name": skill["name"],
        "description": skill["description"],
    }
    fields.update(skill.get("frontmatter_overrides", {}))
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f"{key}: {yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def render_skill(skill: Dict[str, Any]) -> str:
    """Render SKILL.md: frontmatter + skill_body. That's it."""
    if "skill_body" not in skill or not skill["skill_body"].strip():
        raise ValueError(f"Skill '{skill['name']}' is missing required 'skill_body'")
    body = skill["skill_body"].rstrip() + "\n"
    return f"{render_frontmatter(skill)}\n\n{body}"


def render_plain_readme(skill: Dict[str, Any]) -> str:
    """Human-friendly README.md that sits beside SKILL.md for humans browsing the repo."""
    triggers = skill.get("trigger_phrases", [])
    trigger_text = ", ".join(f"`{t}`" for t in triggers) if triggers else "N/A"
    audience = ", ".join(skill.get("audience", []))
    return f"""# {skill['title']}

**Category:** {skill['category']} · **Priority:** {skill.get('priority', 'normal')} · **Audience:** {audience}

{skill['description']}

## When Claude should reach for this

Trigger phrases: {trigger_text}

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
"""


def write_supporting_files(skill: Dict[str, Any], skill_dir: Path) -> Iterable[Path]:
    """Write any supporting files declared in `supporting_files`. Refuse empty stubs."""
    supporting = skill.get("supporting_files", {}) or {}
    written: list[Path] = []
    for rel_path, content in supporting.items():
        if not content or not content.strip():
            raise ValueError(
                f"Skill '{skill['name']}' supporting file '{rel_path}' is empty. "
                "Remove the entry or provide real content."
            )
        target = skill_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip() + "\n")
        written.append(target)
    return written


def write_category_readme(category: str, skills: list[Dict[str, Any]], cat_dir: Path) -> None:
    lines = [
        f"# {CATEGORY_TITLES.get(category, category.title())}",
        "",
        CATEGORY_INTRO.get(category, ""),
        "",
        "## Included skills",
        "",
    ]
    for s in sorted(skills, key=lambda s: s["name"]):
        lines.append(f"- [`{s['name']}/`](./{s['name']}/) — {s['description'].split('.')[0]}.")
    cat_dir.mkdir(parents=True, exist_ok=True)
    (cat_dir / "README.md").write_text("\n".join(lines) + "\n")


def write_root_readme(by_category: Dict[str, list[Dict[str, Any]]]) -> None:
    lines = [
        "# Skills Library",
        "",
        "Installable Claude Code skills grouped by category. Every skill is a directory with a `SKILL.md` (what Claude reads) and a `README.md` (what humans read).",
        "",
        "## Categories",
        "",
    ]
    for category in sorted(by_category):
        intro = CATEGORY_INTRO.get(category, "")
        count = len(by_category[category])
        lines.append(f"- [`{category}/`](./{category}/) — {count} skills. {intro}")
    (SKILLS_ROOT / "README.md").write_text("\n".join(lines) + "\n")


def write_bundle(source_dir: Path, zip_path: Path, prefix: str) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(source_dir.rglob("*")):
            if p.is_file():
                zf.write(p, arcname=str(Path(prefix) / p.relative_to(source_dir)))


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found", file=sys.stderr)
        return 2
    db = json.loads(DB_PATH.read_text())
    skills = db["skills"]

    if SKILLS_ROOT.exists():
        shutil.rmtree(SKILLS_ROOT)
    if BUNDLES_ROOT.exists():
        shutil.rmtree(BUNDLES_ROOT)
    SKILLS_ROOT.mkdir(parents=True, exist_ok=True)
    BUNDLES_ROOT.mkdir(parents=True, exist_ok=True)

    by_category: Dict[str, list[Dict[str, Any]]] = {}
    for skill in skills:
        by_category.setdefault(skill["category"], []).append(skill)

    total = 0
    for category, items in by_category.items():
        cat_dir = SKILLS_ROOT / category
        write_category_readme(category, items, cat_dir)
        for skill in items:
            skill_dir = cat_dir / skill["name"]
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(render_skill(skill))
            (skill_dir / "README.md").write_text(render_plain_readme(skill))
            write_supporting_files(skill, skill_dir)
            total += 1
        # per-category bundle
        write_bundle(cat_dir, BUNDLES_ROOT / f"{category}-skills.zip", prefix=category)

    write_root_readme(by_category)
    # mega-bundle
    write_bundle(SKILLS_ROOT, BUNDLES_ROOT / "all-skills.zip", prefix="skills")

    print(f"Rendered {total} skills across {len(by_category)} categories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
