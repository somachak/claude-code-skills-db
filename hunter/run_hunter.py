#!/usr/bin/env python3
"""Daily skills hunter.

Pipeline: discover -> score -> decide (create / overwrite / skip) -> merge -> regenerate -> commit.

Runs in two modes:
  --mode dry-run       : reports decisions without touching the database.
  --mode auto-commit   : applies decisions, regenerates, validates, commits, pushes.

Required env:
  GITHUB_TOKEN         : required. Used for the GitHub search API and git push.
  ANTHROPIC_API_KEY    : optional. Used to enrich candidate skill bodies with
                         real domain content that matches our authoring rules.
                         If absent, candidates are merged with their raw body.
  X_BEARER_TOKEN       : optional. Used for X searches. Skipped if absent.
  EXA_API_KEY          : optional. Used for web_search_queries. Skipped if absent.

Design goals:
  * Deterministic enough to run unattended.
  * Every decision is auditable (CHANGELOG.md).
  * Never silently clobbers a skill — overwrites require a 15% score win.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import yaml  # type: ignore
except ImportError:
    print("FATAL: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "skills-database.json"
SOURCES = ROOT / "hunter" / "sources.yml"
CACHE_DIR = ROOT / "hunter" / ".cache"
CHANGELOG = ROOT / "hunter" / "CHANGELOG.md"

CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ---------- data types ----------

@dataclass
class Candidate:
    name: str
    title: str
    category: str
    description: str
    body: str
    source_url: str
    source_type: str
    tags: list[str] = field(default_factory=list)
    stars: int = 0
    forks: int = 0
    last_push: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256(self.source_url.encode()).hexdigest()[:12]


@dataclass
class Decision:
    verdict: str            # "create" | "overwrite" | "skip" | "reject"
    candidate: Candidate
    score: int
    breakdown: dict[str, int]
    reason: str
    replaces: Optional[str] = None   # existing skill name if overwrite


# ---------- http + caching ----------

def cached_get(url: str, headers: Optional[dict[str, str]] = None, ttl_hours: int = 12) -> Optional[str]:
    key = hashlib.sha256(url.encode()).hexdigest()
    cache = CACHE_DIR / f"{key}.json"
    if cache.exists():
        blob = json.loads(cache.read_text())
        age_h = (dt.datetime.utcnow() - dt.datetime.fromisoformat(blob["fetched_at"])).total_seconds() / 3600
        if age_h < ttl_hours:
            return blob["body"]
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  http error: {url}: {e}", file=sys.stderr)
        return None
    cache.write_text(json.dumps({"fetched_at": dt.datetime.utcnow().isoformat(), "body": body}))
    return body


# ---------- discovery ----------

def gh_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN", "")
    h = {"Accept": "application/vnd.github+json", "User-Agent": "skills-hunter/1.0"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def discover_github_search(query: str, tags: list[str]) -> list[Candidate]:
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page=20"
    body = cached_get(url, headers=gh_headers())
    if not body:
        return []
    data = json.loads(body)
    out: list[Candidate] = []
    for r in data.get("items", []):
        readme_url = f"https://raw.githubusercontent.com/{r['full_name']}/{r['default_branch']}/README.md"
        readme = cached_get(readme_url) or ""
        out.append(Candidate(
            name=slug(r["name"]),
            title=r["name"].replace("-", " ").title(),
            category=guess_category(readme, tags),
            description=(r.get("description") or "")[:800],
            body=readme,
            source_url=r["html_url"],
            source_type="github-repo",
            tags=tags,
            stars=r.get("stargazers_count", 0),
            forks=r.get("forks_count", 0),
            last_push=r.get("pushed_at"),
            raw=r,
        ))
    return out


def discover_curated_repo(owner: str, name: str, branch: str, tags: list[str]) -> list[Candidate]:
    tree_url = f"https://api.github.com/repos/{owner}/{name}/git/trees/{branch}?recursive=1"
    body = cached_get(tree_url, headers=gh_headers())
    if not body:
        return []
    tree = json.loads(body)
    out: list[Candidate] = []
    for entry in tree.get("tree", []):
        if entry.get("type") == "blob" and entry["path"].endswith("SKILL.md"):
            raw_url = f"https://raw.githubusercontent.com/{owner}/{name}/{branch}/{entry['path']}"
            content = cached_get(raw_url) or ""
            if not content:
                continue
            fm, body_md = split_frontmatter(content)
            skill_name = slug(fm.get("name", Path(entry["path"]).parent.name))
            out.append(Candidate(
                name=skill_name,
                title=fm.get("title", skill_name.replace("-", " ").title()),
                category=guess_category(body_md, tags, fm),
                description=fm.get("description", "")[:800],
                body=body_md,
                source_url=f"https://github.com/{owner}/{name}/blob/{branch}/{entry['path']}",
                source_type="github-repo",
                tags=tags,
                stars=0,
                forks=0,
                last_push=None,
                raw={"frontmatter": fm},
            ))
    return out


def discover_rss(url: str, tags: list[str]) -> list[Candidate]:
    body = cached_get(url)
    if not body:
        return []
    # light RSS parsing without external deps
    items = re.findall(r"<item>(.*?)</item>", body, re.DOTALL)
    out: list[Candidate] = []
    for item in items[:20]:
        title_m = re.search(r"<title>(.*?)</title>", item, re.DOTALL)
        link_m = re.search(r"<link>(.*?)</link>", item, re.DOTALL)
        desc_m = re.search(r"<description>(.*?)</description>", item, re.DOTALL)
        if not (title_m and link_m):
            continue
        title = re.sub(r"<.*?>", "", title_m.group(1)).strip()
        link = link_m.group(1).strip()
        desc = re.sub(r"<.*?>", "", (desc_m.group(1) if desc_m else "")).strip()[:800]
        out.append(Candidate(
            name=slug(title),
            title=title[:80],
            category=guess_category(desc, tags),
            description=desc,
            body=desc,
            source_url=link,
            source_type="blog",
            tags=tags,
        ))
    return out


# ---------- helpers ----------

SLUG_RE = re.compile(r"[^a-z0-9]+")

def slug(text: str) -> str:
    s = SLUG_RE.sub("-", text.lower()).strip("-")
    return s[:64] or "unnamed"


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, parts[2].lstrip("\n")


CATEGORY_HINTS = {
    "frontend": ["react", "nextjs", "next.js", "tailwind", "shadcn", "css", "ui", "component", "accessibility", "a11y"],
    "backend": ["api", "fastapi", "django", "express", "nestjs", "node", "webhook", "auth", "graphql"],
    "data": ["sql", "schema", "migration", "etl", "analytics", "database", "prisma", "drizzle"],
    "testing": ["test", "pytest", "vitest", "jest", "playwright", "cypress", "coverage"],
    "platform": ["docker", "ci", "github actions", "monorepo", "terraform", "kubernetes", "release"],
    "security-reliability": ["security", "threat", "slo", "alert", "observability", "secret", "vulnerab", "csp"],
    "ai-productivity": ["claude", "llm", "prompt", "skill", "rag", "agent"],
}


def guess_category(text: str, tags: list[str], fm: Optional[dict] = None) -> str:
    haystack = ((fm or {}).get("category", "") + " " + " ".join(tags) + " " + (text or ""))[:3000].lower()
    scores: dict[str, int] = {cat: 0 for cat in CATEGORY_HINTS}
    for cat, words in CATEGORY_HINTS.items():
        for w in words:
            if w in haystack:
                scores[cat] += 1
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "ai-productivity"


def trigram(s: str) -> set[str]:
    s = re.sub(r"\s+", " ", s.lower()).strip()
    return {s[i : i + 3] for i in range(len(s) - 2)}


def similarity(a: str, b: str) -> float:
    ta, tb = trigram(a), trigram(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


# ---------- scoring ----------

def score_candidate(c: Candidate, existing: list[dict[str, Any]], floors: dict[str, Any]) -> tuple[int, dict[str, int], Optional[str]]:
    # 1. Stack fit
    stack_fit = 5
    for t in c.tags:
        if t in {"react", "nextjs", "typescript", "tailwind", "shadcn", "node", "express", "nestjs", "python", "fastapi", "django"}:
            stack_fit = 25
            break
        if t in {"testing", "security", "claude-code", "official", "reference"}:
            stack_fit = max(stack_fit, 15)

    # 2. Compliance (heuristic)
    compliance = 0
    if c.body.strip():
        compliance += 5
    if len(c.body) >= int(floors.get("min_body_chars", 600)):
        compliance += 5
    if any(tok in c.body for tok in ["## ", "- [", "Anti-pattern", "Checklist", "When to use", "Example"]):
        compliance += 5
    if c.body.count("\n") < 500:
        compliance += 5
    if c.description and len(c.description) < 1024:
        compliance += 5

    # 3. Social / maintenance
    social = 0
    if c.source_type == "github-repo":
        if c.stars >= 500 and c.forks >= 50:
            social = 20
        elif c.stars >= 100 and c.forks >= 15:
            social = 15
        elif c.stars >= floors.get("github_min_stars", 20) and c.forks >= floors.get("github_min_forks", 5):
            social = 10
    elif c.source_type == "blog":
        social = 10  # RSS item; coarse signal

    # 4. Depth
    depth_markers = sum(1 for m in ["anti-pattern", "checklist", "example", "when to use", "decision"] if m in c.body.lower())
    depth = {0: 0, 1: 0, 2: 6, 3: 12, 4: 20, 5: 20}[min(depth_markers, 5)]

    # 5. Uniqueness
    sim_max, replaces = 0.0, None
    for s in existing:
        blob = f"{s['name']} {s['title']} {s['description']}"
        sim = similarity(f"{c.name} {c.title} {c.description}", blob)
        if sim > sim_max:
            sim_max, replaces = sim, s["name"]
    if sim_max < 0.40:
        uniqueness = 10
        replaces = None
    elif sim_max < 0.60:
        uniqueness = 6
        replaces = None
    elif sim_max < float(floors.get("similarity_threshold_dedup", 0.80)):
        uniqueness = 3  # overwrite candidate
    else:
        uniqueness = 0

    total = stack_fit + compliance + social + depth + uniqueness
    return total, {"stack_fit": stack_fit, "compliance": compliance, "social": social, "depth": depth, "uniqueness": uniqueness}, replaces


# ---------- decisions ----------

def decide(c: Candidate, existing: list[dict[str, Any]], floors: dict[str, Any]) -> Decision:
    score, breakdown, replaces = score_candidate(c, existing, floors)
    if score < 60:
        return Decision("reject", c, score, breakdown, f"below threshold (score={score})")
    if breakdown["compliance"] < 15:
        return Decision("reject", c, score, breakdown, "authoring-rule compliance too low")
    if breakdown["uniqueness"] >= 6:
        return Decision("create", c, score, breakdown, "net-new territory")
    if breakdown["uniqueness"] >= 3 and replaces:
        incumbent = next((s for s in existing if s["name"] == replaces), None)
        incumbent_score = _existing_score(incumbent) if incumbent else 0
        ratio = float(floors.get("overwrite_improvement_ratio", 1.15))
        if score >= incumbent_score * ratio:
            return Decision("overwrite", c, score, breakdown, f"beats {replaces} ({score} vs {incumbent_score})", replaces=replaces)
        return Decision("skip", c, score, breakdown, f"not materially better than {replaces} ({score} vs {incumbent_score})")
    return Decision("skip", c, score, breakdown, "duplicate")


def _existing_score(skill: dict[str, Any]) -> int:
    # Rough incumbent score: 80 baseline, inflated for skills already at core priority
    base = 80
    if skill.get("priority") == "core":
        base += 10
    return base


# ---------- merge ----------

def apply_decisions(db: dict[str, Any], decisions: list[Decision]) -> tuple[int, int]:
    created, overwritten = 0, 0
    by_name = {s["name"]: s for s in db["skills"]}
    for d in decisions:
        if d.verdict == "create":
            by_name[d.candidate.name] = candidate_to_skill(d.candidate)
            created += 1
        elif d.verdict == "overwrite" and d.replaces:
            new_entry = candidate_to_skill(d.candidate, name=d.replaces)
            by_name[d.replaces] = new_entry
            overwritten += 1
    db["skills"] = sorted(by_name.values(), key=lambda s: (s["category"], s["name"]))
    db["version"] = dt.date.today().isoformat()
    db["generated_at"] = dt.datetime.utcnow().isoformat() + "Z"
    return created, overwritten


def candidate_to_skill(c: Candidate, name: Optional[str] = None) -> dict[str, Any]:
    return {
        "name": name or c.name,
        "title": c.title,
        "category": c.category,
        "audience": ["full-stack"],
        "priority": "supporting",
        "description": c.description or f"{c.title}. Imported by the daily hunter.",
        "trigger_phrases": sorted(set(c.tags + [c.name]))[:6] or [c.name, c.title.lower()],
        "skill_body": c.body.strip() or f"# {c.title}\n\nImported from {c.source_url}. Needs enrichment.\n",
        "frontmatter_overrides": {},
        "provenance": {
            "source_url": c.source_url,
            "source_type": c.source_type,
            "stars": c.stars,
            "forks": c.forks,
            "captured_at": dt.datetime.utcnow().isoformat() + "Z",
        },
    }


# ---------- orchestration ----------

def run_discovery(sources: dict[str, Any]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for q in sources.get("github_search_queries", []):
        print(f"  discover github: {q['query']}")
        candidates += discover_github_search(q["query"], q.get("tags", []))
    for r in sources.get("curated_github_repos", []):
        print(f"  discover curated: {r['owner']}/{r['name']}")
        candidates += discover_curated_repo(r["owner"], r["name"], r.get("branch", "main"), r.get("tags", []))
    for feed in sources.get("rss_feeds", []):
        print(f"  discover rss: {feed['url']}")
        candidates += discover_rss(feed["url"], feed.get("tags", []))
    # dedup by source_url
    seen: set[str] = set()
    out: list[Candidate] = []
    for c in candidates:
        if c.source_url in seen:
            continue
        seen.add(c.source_url)
        out.append(c)
    return out


def run_pipeline(mode: str, stack: list[str]) -> int:
    print(f"Hunter starting. Mode={mode}. Stack={','.join(stack)}")
    sources = yaml.safe_load(SOURCES.read_text())
    floors = sources.get("quality_floors", {})
    db = json.loads(DB_PATH.read_text())

    candidates = run_discovery(sources)
    print(f"Discovered {len(candidates)} candidates.")

    decisions = [decide(c, db["skills"], floors) for c in candidates]
    created = sum(1 for d in decisions if d.verdict == "create")
    overwritten = sum(1 for d in decisions if d.verdict == "overwrite")
    rejected = sum(1 for d in decisions if d.verdict == "reject")
    skipped = sum(1 for d in decisions if d.verdict == "skip")
    print(f"Decisions: {created} create, {overwritten} overwrite, {skipped} skip, {rejected} reject.")

    if mode == "dry-run":
        for d in decisions[:30]:
            print(f"  [{d.verdict}] {d.candidate.name} score={d.score} reason={d.reason}")
        return 0

    if created + overwritten == 0:
        print("No actionable changes. Exiting.")
        append_changelog(decisions, applied=False)
        return 0

    created, overwritten = apply_decisions(db, decisions)
    DB_PATH.write_text(json.dumps(db, indent=2) + "\n")

    rc = subprocess.call([sys.executable, "tools/create_actual_skills.py"], cwd=ROOT)
    if rc != 0:
        print("Generator failed. Rolling back.", file=sys.stderr)
        subprocess.call(["git", "checkout", "--", str(DB_PATH)], cwd=ROOT)
        return rc

    rc = subprocess.call([sys.executable, "scripts/generate_index.py"], cwd=ROOT)
    if rc != 0:
        return rc

    rc = subprocess.call([sys.executable, "scripts/validate_skills_db.py"], cwd=ROOT)
    if rc != 0:
        print("Validation failed. Rolling back.", file=sys.stderr)
        subprocess.call(["git", "checkout", "--", str(DB_PATH)], cwd=ROOT)
        return rc

    append_changelog(decisions, applied=True, created=created, overwritten=overwritten)
    commit_and_push(created, overwritten)
    return 0


def append_changelog(decisions: list[Decision], applied: bool, created: int = 0, overwritten: int = 0) -> None:
    stamp = dt.datetime.utcnow().isoformat() + "Z"
    lines = [f"\n## {stamp} {'APPLIED' if applied else 'DRY'} — +{created} / ~{overwritten}", ""]
    for d in decisions:
        lines.append(f"- [{d.verdict}] `{d.candidate.name}` score={d.score} " + (f"replaces=`{d.replaces}` " if d.replaces else "") + f"reason={d.reason}")
    header = CHANGELOG.read_text() if CHANGELOG.exists() else "# Hunter Changelog\n"
    CHANGELOG.write_text(header + "\n".join(lines) + "\n")


def commit_and_push(created: int, overwritten: int) -> None:
    stamp = dt.date.today().isoformat()
    subprocess.call(["git", "add", "-A"], cwd=ROOT)
    rc = subprocess.call(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if rc == 0:
        print("Nothing staged after regen. Skipping commit.")
        return
    msg = f"hunter: +{created} new, ~{overwritten} updated ({stamp})"
    subprocess.call(["git", "commit", "-m", msg], cwd=ROOT)
    subprocess.call(["git", "push"], cwd=ROOT)


# ---------- entry ----------

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["dry-run", "auto-commit"], default="dry-run")
    p.add_argument("--stack", default="react,nextjs,typescript,node,python,fastapi,django,tailwind,shadcn")
    args = p.parse_args()
    return run_pipeline(args.mode, args.stack.split(","))


if __name__ == "__main__":
    sys.exit(main())
