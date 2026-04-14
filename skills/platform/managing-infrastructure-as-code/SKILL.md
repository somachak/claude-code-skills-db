---
name: managing-infrastructure-as-code
description: Reviews infrastructure code for modularity, environment separation, drift risk, secret handling, and safe rollout patterns. Use when working with Terraform, Pulumi, or cloud templates.
when_to_use: terraform review, pulumi, iac
allowed-tools: Bash Read
---

## Terraform, Pulumi, or CloudFormation

Infrastructure as Code treats infrastructure like software: version-controlled, reviewed, tested. The skill is designing repeatable, safe infrastructure deployments.

### When to Use

- Managing cloud resources (AWS, GCP, Azure)
- Ensuring consistency across environments
- Disaster recovery and scaling

### Decision Framework for Terraform

1. **State is sacred.** Terraform state file knows what resources exist. Modify via Terraform, not by hand. Corruption = destroyed resources.
2. **Modules for composition.** Reusable infrastructure components (networking, database, app service). Reduces duplication.
3. **Plan before apply.** `terraform plan` shows changes. Review, approve, then `terraform apply`. Prevents accidents.
4. **State is remote and locked.** Store in S3 (with backend locking), not locally. Multiple people can use same state safely.
5. **Drift detection.** Periodically run `terraform plan`; if resources changed outside Terraform, alert. Keep code and reality in sync.

### Anti-patterns to Avoid

- Manual infrastructure changes. Infrastructure drifts from code. Can't reproduce.
- No plan review. Apply directly to production. Oops, deleted database.
- State in local Git. Multiple people modify; conflicts and corruption.

### Checklist

- [ ] Infrastructure is code (Terraform, Pulumi, or CloudFormation)
- [ ] All resources are managed via IaC (no manual console changes)
- [ ] Plan is reviewed before apply
- [ ] State is stored remotely with locking (S3 + DynamoDB)
- [ ] Environments (dev, staging, prod) use same code (different var files)
- [ ] Secrets (API keys, passwords) are managed securely (not in code)
- [ ] Drift detection runs regularly
- [ ] Rollback procedure is tested
