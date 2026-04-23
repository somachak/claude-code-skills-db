---
name: release-lifecycle-manager
description: "Manages the full software release lifecycle: semantic versioning, conventional commits, automated changelog generation, release readiness gates, hotfix procedures, and rollback triggers. Use when shipping a versioned release, coordinating a hotfix, writing a changelog, or establishing a release process for a team. Different from running-release-checklists which executes a single pre-release checklist. Covers Git Flow, trunk-based, and GitHub Flow workflows."
---

# Release Lifecycle Manager

Full software release lifecycle — from commit convention through hotfix and rollback.

## When to Use

- Determining the next semantic version from commit history
- Generating a changelog automatically from conventional commits
- Planning a release: readiness gates, stakeholder communication, deployment sequencing
- Managing a P0/P1 hotfix under pressure
- Establishing a release process for a new team or project
- Setting rollback triggers before a deployment

## When NOT to Use

- Executing a pre-existing deployment runbook — use running-release-checklists skill
- CI/CD pipeline setup — use hardening-ci-pipelines skill
- Container image publishing — use docker-optimization or shipping-containerized-services

## Semantic Versioning Rules

MAJOR.MINOR.PATCH:
- **MAJOR**: breaking change — callers must update. Increment when removing/renaming a public API, changing a function signature incompatibly, or changing behavior that breaks existing clients.
- **MINOR**: new capability, backward compatible. Increment when adding new endpoints, fields, or features; or deprecating (but not removing) an API.
- **PATCH**: bug fix, backward compatible. Increment when fixing incorrect behavior without changing the interface.

Pre-release labels: `1.2.0-alpha.1`, `1.2.0-beta.3`, `1.2.0-rc.1`

## Conventional Commits (Required for Automation)

Format: `<type>(<scope>): <description>`

| Type | Version Impact | Changelog Section |
|------|---------------|-------------------|
| `feat` | MINOR | Features |
| `fix` | PATCH | Bug Fixes |
| `perf` | PATCH | Performance |
| `refactor` | none | Internal |
| `test` | none | (omitted) |
| `docs` | none | Documentation |
| `BREAKING CHANGE` footer | MAJOR | Breaking Changes |

Automated version bump logic: scan commits since last tag. Any `BREAKING CHANGE` footer -> MAJOR. Any `feat` -> MINOR. Otherwise -> PATCH.

## Release Readiness Gates

Before cutting a release, all gates must pass:
- [ ] Test coverage at or above threshold (typically 85%)
- [ ] Zero open P0/P1 bugs in the milestone
- [ ] All feature flags for this release tested in staging
- [ ] Database migrations tested on a staging copy of production data
- [ ] Rollback procedure documented and tested (not just written)
- [ ] Stakeholder sign-off (PM + relevant team leads)
- [ ] Monitoring/alerting deployed for new features
- [ ] Runbook updated for any new operational dependencies

## Release Workflows

**Trunk-based (recommended for fast teams):**
- All work lands on `main` via short-lived branches
- Release from `main` at any time by tagging
- Hotfixes: cherry-pick to `main`, tag immediately

**Git Flow (recommended for versioned products):**
- Feature branches into `develop`, then `release/x.y.z`, then `main`
- Hotfix branches from `main`, merged back to `main` AND `develop`

**GitHub Flow (recommended for SaaS with continuous deployment):**
- All branches from `main`, merge via PR, deploy on merge

## Hotfix Procedure

| Severity | Definition | SLA |
|----------|-----------|-----|
| P0-Critical | Data loss, security breach, complete service down | Deploy within 2 hours |
| P1-High | Key feature broken for >10% of users | Deploy within 8 hours |
| P2-Medium | Degraded feature, workaround exists | Next planned release |

P0/P1 hotfix steps:
1. Create `hotfix/description` branch from the release tag (not main/develop)
2. Apply minimal fix — no new features, no refactors
3. Write a regression test that would have caught the bug
4. Fast-track review: two engineers, 30-min SLA for P0
5. Deploy to staging, run smoke tests, deploy to production
6. Cherry-pick or merge back to main AND develop/trunk
7. Tag a new PATCH release immediately

## Rollback Triggers

Define rollback triggers BEFORE deploying:
- Error rate exceeds threshold (e.g., 2x baseline)
- p95 latency exceeds SLO threshold (e.g., 2x normal)
- Any P0 alert firing
- Synthetic monitor failure in production

Rollback options: feature flags (flip off), blue/green (redirect traffic back), image rollback (redeploy previous tag).

## Changelog Template

```markdown
## [1.3.0] - 2026-04-23

### Breaking Changes
- Renamed user.email to user.primaryEmail in all API responses (#234)

### Features
- Add bulk export endpoint for audit logs (#221)
- Support OAuth2 PKCE flow for mobile clients (#228)

### Bug Fixes
- Fix pagination cursor wrapping on last page (#230)
- Correct timezone handling in scheduled job triggers (#225)

### Performance
- Cut p99 latency on /search by 40% with index optimization (#219)
```

## Stakeholder Communication Templates

**Pre-release (24h before):**
Release X.Y.Z deploys tomorrow at [time]. Changes: [2-line summary]. Downtime: none expected. Rollback: available within 5 min if needed.

**Post-release:**
X.Y.Z is live. [Key features]. Monitoring looks nominal. [Link to changelog].

**Hotfix:**
P1 hotfix deploying now for [issue]. ETA: [time]. Impact: [who is affected]. Mitigation available: [workaround if any].
