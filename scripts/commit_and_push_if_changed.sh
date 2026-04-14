#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/user/workspace/claude-code-skills-db"
cd "$REPO_DIR"

git config user.name "Perplexity Computer"
git config user.email "pixelartinc@gmail.com"

git add skills-database.json skills-schema.json README.md daily-update-playbook.md cron-task-spec.md scripts/validate_skills_db.py scripts/commit_and_push_if_changed.sh

if git diff --cached --quiet; then
  echo "NO_CHANGES_TO_COMMIT"
  exit 0
fi

STAMP=$(date -u +"%Y-%m-%d")
git commit -m "Daily update: refresh Claude Code skills database (${STAMP})"
git push origin main

echo "PUSHED_UPDATES"
