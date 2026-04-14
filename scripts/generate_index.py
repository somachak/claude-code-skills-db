#!/usr/bin/env python3
"""Generate SKILLS_INDEX.md from skills-database.json.

A single flat, searchable index of every skill in the library.
Rebuilt on every generator run so it never drifts from the source of truth.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = json.loads((ROOT / "skills-database.json").read_text())

def fmt_triggers(triggers):
    return ", ".join(f"`{t}`" for t in triggers[:6]) + ("..." if len(triggers) > 6 else "")

def main() -> int:
    skills = DB["skills"]
    by_cat = defaultdict(list)
    for s in skills:
        by_cat[s["category"]].append(s)

    lines = [
        "# Skills Index",
        "",
        f"_{len(skills)} skills across {len(by_cat)} categories. Generated from `skills-database.json` — do not edit by hand._",
        "",
        f"**Version:** `{DB.get('version', 'unversioned')}` · **Last generated:** `{DB.get('generated_at', 'unknown')}`",
        "",
        "## Quick search",
        "",
        "| Skill | Category | Priority | Description |",
        "|---|---|---|---|",
    ]
    for s in sorted(skills, key=lambda x: (x["category"], x["name"])):
        desc = s["description"].split(". ")[0].replace("|", "\\|")
        link = f"[`{s['name']}`](./skills/{s['category']}/{s['name']}/SKILL.md)"
        lines.append(f"| {link} | {s['category']} | {s['priority']} | {desc} |")

    lines += ["", "## By category", ""]
    for cat in sorted(by_cat):
        lines.append(f"### {cat}")
        lines.append("")
        for s in sorted(by_cat[cat], key=lambda x: x["name"]):
            lines.append(f"- **[`{s['name']}`](./skills/{cat}/{s['name']}/SKILL.md)** — {s['description']}")
            lines.append(f"  · triggers: {fmt_triggers(s['trigger_phrases'])}")
        lines.append("")

    out = ROOT / "SKILLS_INDEX.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out.relative_to(ROOT)} ({len(skills)} skills)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
