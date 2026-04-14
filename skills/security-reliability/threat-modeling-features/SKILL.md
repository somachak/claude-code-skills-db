---
name: threat-modeling-features
description: Threat-models new features by identifying assets, trust boundaries, attack paths, and mitigations. Use when reviewing auth changes, payments, admin tools, integrations, or other sensitive workflows.
when_to_use: threat model, attack surface, security review
allowed-tools: Read Grep
---

## Identifying and Mitigating Threats

Threat modeling anticipates attacks before code is written. The skill is identifying attack vectors (data breach, DoS, privilege escalation) and mitigating them early.

### When to Use

- Designing new features (payment, auth, admin panel)
- Security review before launch
- Incident post-mortem: "How do we prevent this?"

### Decision Framework

1. **STRIDE framework.** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. Ask: which threats apply?
2. **Trust boundaries.** Data crossing boundary = potential attack. User input → database: sanitize. User upload → storage: scan. External API → app: validate.
3. **Least privilege.** User has only permissions they need. Payment service doesn't need to delete users. Limits blast radius.
4. **Defense in depth.** Multiple layers. Firewall + authentication + rate limiting + encryption. One layer fails, others protect.
5. **Assume breach.** What if attacker is inside? Encryption at rest, audit logs, alerting on anomalies.

### Anti-patterns to Avoid

- Security as afterthought. Design without threat modeling; fix vulnerabilities after launch.
- Trusting user input. "Users are good" or "We validate on frontend." Backend must validate.
- Single point of failure. Authentication only via password. MFA is secondary.

### Checklist

- [ ] STRIDE threats for feature are identified (Spoofing, Tampering, etc.)
- [ ] Trust boundaries are drawn; data crossing them is validated
- [ ] Least privilege is applied (user has minimal permissions)
- [ ] Authentication and authorization are enforced server-side
- [ ] Sensitive data is encrypted (at rest and in transit)
- [ ] Rate limiting prevents brute force and DoS
- [ ] Audit logs record sensitive actions
- [ ] Incident response plan exists (if breach detected, what's the playbook?)
