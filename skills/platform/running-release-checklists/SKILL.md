---
name: running-release-checklists
description: Runs release preparation checklists covering quality gates, migrations, rollback readiness, communication, and post-release verification. Use when preparing staging or production releases.
when_to_use: release checklist, go live, rollback plan
allowed-tools: Bash Read
---

## Versioning, Changelogs, and Release Coordination

Releases are high-stakes events. Mistakes (missing migration, wrong version number) cause downtime. The skill is running checklists, automating where possible, and maintaining a clear changelog.

### When to Use

- Preparing a release (new version, multiple PRs)
- Coordinating cross-team deployments
- Documenting changes for users

### Decision Framework for Semantic Versioning and Changelogs

1. **Semantic Versioning (SemVer).** MAJOR.MINOR.PATCH. MAJOR for breaking changes, MINOR for features, PATCH for fixes. Users understand impact.
2. **Changelog is manual effort.** Auto-generated from commits is noisy. Humans write clear, user-facing summary. Keep CHANGELOG.md.
3. **Release checklist is explicit.** Version bump, changelog update, migrations, feature flags OFF, staged deploy, production deploy, rollback plan. Run in order.
4. **Dry-run release in staging.** Deploy to staging, run smoke tests, verify no errors. Then confidently deploy to production.
5. **Announce releases.** Slack notification, email, blog post. Users (customers, team) know what changed and why.

### Anti-patterns to Avoid

- Ad-hoc releases. "Let's just deploy" without checklist. Forgotten migration = downtime.
- No changelog. Users don't know what changed. Support gets flooded with questions.
- Version mismatch. Code is v2.1, deployed v2.0. Confusion and bugs.

### Checklist

- [ ] Version number is bumped (SemVer)
- [ ] CHANGELOG.md is updated with user-facing summary
- [ ] All migrations are ready (if database changes)
- [ ] Feature flags for new features are OFF by default
- [ ] Staged deploy runs smoke tests (OK)
- [ ] Production deploy plan is documented (steps, rollback)
- [ ] Team is notified (Slack, email)
- [ ] Rollback procedure is tested and ready
