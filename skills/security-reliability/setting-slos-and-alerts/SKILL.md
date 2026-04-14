---
name: setting-slos-and-alerts
description: Designs service-level objectives, indicators, and actionable alerts that reduce noise and improve operational focus. Use when tuning monitoring for APIs, background systems, or customer-facing journeys.
when_to_use: slo, alert fatigue, slis
allowed-tools: Read Grep
---

## Service Level Objectives and Alerting

SLOs (Service Level Objectives) define acceptable uptime and performance. Alerting tells you when you breach SLOs. The skill is setting realistic SLOs and responding to breaches.

### When to Use

- Defining service reliability targets
- Incident response and on-call
- Capacity planning and scaling

### Decision Framework

1. **SLO is realistic.** 99.9% uptime (8.76 hours downtime/year) vs. 99.99% (52 minutes/year). Business impact determines target.
2. **Error budget.** If SLO is 99.9%, you have 8.76 hours of downtime/year. Spend it on deploys, maintenance. Overspend = SLO breach.
3. **Alerts are high-fidelity.** Alert when SLO is at risk, not on every blip. False alarms = on-call fatigue.
4. **Runbook exists.** Alert fires; on-call has procedure: check logs, restart service, page engineer. No guessing.
5. **Blameless post-mortems.** When SLO breaches, investigate and learn. No blame; fix systemic issues.

### Anti-patterns to Avoid

- SLO too strict. 99.99% for non-critical service = constant alerting, no one responds.
- Alerts everywhere. Alert fatigue; on-call ignores them.
- No error budget concept. Deploy conservatively even if reliability allows risk-taking.

### Checklist

- [ ] SLO is defined per service (uptime, latency, error rate)
- [ ] SLO is realistic and matches business needs
- [ ] Error budget is tracked and communicated
- [ ] Alerts are configured for SLO breaches (high-fidelity, low false positive rate)
- [ ] Runbook exists for critical alerts
- [ ] On-call rotation is clear (who's on-call, how to escalate)
- [ ] Incident response process is documented
- [ ] Post-mortems are conducted (no blame, focus on improvements)
