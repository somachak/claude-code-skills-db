---
name: hardening-ci-pipelines
description: Improves CI pipelines for speed, reliability, caching, matrix strategy, and failure isolation. Use when builds are slow, flaky, expensive, or hard to trust.
when_to_use: ci pipeline, github actions, flaky build
allowed-tools: Bash Read
---

## Build, Test, Deploy Safety

CI/CD pipelines are the blast radius for code changes. A compromised pipeline = compromised app. The skill is designing pipelines for reliability, security, and fast feedback.

### When to Use

- Setting up CI/CD for a new project
- Auditing pipeline for security and reliability
- Reducing pipeline failures or duration

### Decision Framework for GitHub Actions, GitLab CI, or CircleCI

1. **Secrets are not in code.** Use secret management (AWS Secrets Manager, HashiCorp Vault). CI/CD system (GitHub Actions) provides secret injection.
2. **Artifact integrity.** Build artifact should be reproducible. Dockerfile fingerprint doesn't change unless code or dependencies change.
3. **Test gates before deploy.** Unit tests → integration tests → staging deploy → smoke tests → production deploy. Each gate must pass.
4. **Permissions are minimal.** Deploy step requires manual approval. Automated rollback on error.
5. **Status checks are visible.** Every PR shows CI status. Can't merge without passing tests.

### Anti-patterns to Avoid

- Secrets in code or config files. CI/CD logs are often visible.
- Non-deterministic builds. Build same code twice, get different artifact. Hard to debug.
- No tests before deploy. Tests run after merge. If test fails, bug is in production.

### Checklist

- [ ] Secrets are injected via CI/CD secret management
- [ ] Build is deterministic (same code = same artifact)
- [ ] Dockerfile or build script is version-controlled
- [ ] Unit and integration tests run before merge
- [ ] Staging deploy runs smoke tests
- [ ] Deploy to production requires approval
- [ ] Deployment is logged (who, when, what changed)
- [ ] Rollback procedure is automated and tested
