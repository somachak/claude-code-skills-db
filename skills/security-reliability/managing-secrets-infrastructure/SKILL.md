---
name: managing-secrets-infrastructure
description: "Designs and audits secrets infrastructure at scale: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager. Use when moving beyond .env files to production secrets management — dynamic credentials, automatic rotation, audit logging, and CI/CD integration without long-lived tokens. Covers AppRole auth, Kubernetes pod identities, dynamic database credentials, certificate lifecycle, and 15-minute emergency rotation procedures. Different from auditing-secrets-and-config which audits existing code-level practices."
---

# Managing Secrets Infrastructure

Design and operate production secrets management beyond .env files. Infrastructure-scale: Vault, cloud KMS, dynamic credentials, rotation automation.

## When to Use

- Moving from .env files or hardcoded secrets to production secrets management
- Setting up HashiCorp Vault or cloud secret stores (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)
- Implementing dynamic database credentials (short-lived, auto-rotated)
- Integrating secrets into CI/CD pipelines without long-lived tokens
- Designing secret rotation without downtime
- Responding to a suspected secret leak (15-minute containment procedure)

## When NOT to Use

- Auditing existing secret handling in application code — use auditing-secrets-and-config skill
- Application-level API key management — use auditing-secrets-and-config skill
- This skill is for infrastructure setup, not code review

## Anti-Patterns

- **Long-lived service credentials** — use dynamic credentials that expire in minutes/hours
- **Single-person Vault unseal** — one sick engineer blocks all ops. Use Shamir secret sharing (minimum 3-of-5) or cloud KMS auto-unseal.
- **No audit devices** — you cannot investigate a breach without audit logs. Configure two audit backends on day one.
- **Secrets in CI/CD env vars** — visible in logs, stored indefinitely. Use OIDC token exchange or Vault Agent instead.
- **Overly permissive policies** — a compromised service with `path "*" { capabilities = ["*"] }` gets everything. Scope to the minimum paths required.
- **Untested rotation** — rotation that has never been tested will fail in an emergency. Schedule quarterly rotation drills.

## Vault Architecture Decision

**HA Raft deployment (recommended):**
- 3 or 5 node cluster with Raft integrated storage
- Cloud KMS auto-unseal (AWS KMS / GCP Cloud KMS / Azure Key Vault)
- Environment-based namespaces: ns/production, ns/staging, ns/dev
- Two audit log destinations: file (local) + syslog/SIEM

**Managed alternatives (simpler, less flexible):**
- AWS Secrets Manager: best when fully on AWS, pay-per-secret model
- GCP Secret Manager: best when fully on GCP, flat pricing
- Azure Key Vault: best for Azure workloads, HSM-backed option

**Decision rule**: use Vault when you need dynamic credentials, multiple clouds, or fine-grained policy control. Use cloud-managed when single-cloud and ops simplicity outweighs flexibility.

## Authentication Methods

AppRole for service-to-service: use short-lived secret IDs (10m TTL), 1h token TTL, policy scoped to the service's paths only.

Kubernetes pod identity: bind to specific service account names and namespaces. Token TTL 1h.

OIDC for human operators via Okta/Google: maps groups to Vault policies. Never use userpass auth in production — OIDC provides MFA and session management.

## Dynamic Credentials (The Key Pattern)

Dynamic database credentials give each service request a unique, expiring PostgreSQL role:
- creation_statements creates a role VALID UNTIL expiration
- default_ttl of 1h means a compromised credential expires automatically
- Revoke immediately if a breach is suspected — no rotation needed, credential is already time-bounded

Apply the same pattern for: AWS IAM tokens (STS), SSH certificates (24h TTL per session), PKI certificates.

## Rotation Strategy by Type

| Type | Strategy | Frequency |
|------|----------|-----------|
| DB passwords | Dual-account swap: create new, verify, delete old | Automatic via Vault |
| API keys | Overlap window: create new, update consumers, revoke old | 90 days |
| TLS certificates | Auto-renew 60 days before expiry via PKI engine | Continuous |
| SSH keys | Short-lived certs via Vault SSH engine (24h TTL) | Per-session |

## CI/CD Integration (No Long-Lived Tokens)

GitHub Actions: use hashicorp/vault-action with JWT method. The OIDC token from GitHub authenticates to Vault, retrieves the secret, and the token expires after the job. No stored credentials.

Kubernetes: use External Secrets Operator with a ClusterSecretStore pointing to Vault. Secrets sync automatically with a configurable refresh interval.

## Emergency Response: Leaked Secret (15-Minute Containment)

1. **0-5 min**: Identify the affected credential. Revoke immediately in Vault (`vault lease revoke`) or cloud console.
2. **5-10 min**: Generate replacement credential. Update all consumers (Kubernetes secrets, env vars, config).
3. **10-15 min**: Rotate the root credential for the affected secret engine. Verify audit logs for any use of the leaked credential in the past 24h.
4. **Post-incident**: Review how the secret leaked (git history, logs, clipboard). Add detection rule to prevent recurrence.

## Vault Unseal Checklist

```
vault status                     # check seal status
vault operator unseal $KEY_1     # requires threshold shares
vault operator unseal $KEY_2
vault operator unseal $KEY_3
vault status | grep Sealed       # must output: Sealed false
vault auth list                  # must show auth methods
vault secrets list               # must show secret engines
```
