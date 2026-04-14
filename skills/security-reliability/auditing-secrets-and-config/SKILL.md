---
name: auditing-secrets-and-config
description: Audits secret handling, environment configuration, rotation practices, and accidental exposure risks. Use when reviewing repositories, deployment configs, CI, or incident follow-up.
when_to_use: secrets audit, env vars, credential exposure
allowed-tools: Read Grep
---

## Secret Management and Configuration

Secrets (API keys, passwords, database credentials) are targets. Config (feature flags, endpoints) changes between environments. The skill is separating them from code and rotating frequently.

### When to Use

- Onboarding service (needs database credentials)
- Rotating credentials (monthly, after departure)
- Auditing for exposed secrets

### Decision Framework for AWS Secrets Manager, HashiCorp Vault, or similar

1. **Secrets are never in code.** Git history is forever. One leaked secret = account compromise. Use secret manager.
2. **Config via environment variables.** `process.env.DATABASE_URL`, `process.env.STRIPE_API_KEY`. Different values per environment.
3. **Least privilege for services.** Database user has only SELECT, not DROP. API service has only its API key, not admin key.
4. **Rotation schedule.** Database passwords rotated monthly. API keys rotated quarterly. If leaked, damage is limited.
5. **Audit logs for access.** Who accessed which secret? Alert on unusual access patterns.

### Anti-patterns to Avoid

- Secrets in code or .env files. Git history or accidental pushes = leak.
- One shared secret for all services. If leaked, all services are compromised.
- No rotation. Secret compromised a year ago; still active.
- No audit logs. Can't detect breach or investigate.

### Checklist

- [ ] No secrets in Git history (`git log -p --all | grep -i password`)
- [ ] Secrets are in secret manager (AWS Secrets Manager, Vault)
- [ ] Config is via environment variables
- [ ] `.env.example` exists (no real secrets); checked in
- [ ] Least privilege for service credentials
- [ ] Secrets are rotated monthly
- [ ] Audit logs for secret access
- [ ] Leaked secret procedure is documented (revoke, rotate, investigate)
- [ ] Test: try to access secret without permission; verify denied
