---
name: turning-runbooks-into-skills
description: Converts operational runbooks into reusable skills with standing instructions, validator loops, and safe invocation controls. Use when a manual checklist is repeated often enough to automate guidance.
when_to_use: runbook to skill, operational checklist, codify process
---

## Automation from Manual Procedures

Runbooks are procedures (incident response, deployment, backups). Skills automate them. The skill is identifying automation opportunities and building reliable automation.

### When to Use

- Runbook is followed >1x/month
- Runbook is error-prone (forgotten steps, manual mistakes)
- Runbook is long (>10 steps)

### Decision Framework

1. **Runbook step → skill command.** Manual: "SSH to server, check logs, restart." Skill: "Check logs for errors, alert if restart needed."
2. **Idempotency is essential.** Skill runs twice (accidental re-trigger)? Same result. No side effects.
3. **Observability is built-in.** Skill logs actions taken (what was done, why, result). On-call can see what happened.
4. **Fallback is manual.** Skill automates happy path. If something's wrong, escalate to human. Don't blindly execute.
5. **Skill is tested in staging first.** Before trusting automation in production, test on staging.

### Anti-patterns to Avoid

- Blind automation. Skill executes without validation. Corrupt state = disaster.
- Non-idempotent automation. Skill runs twice; creates duplicate entries or state conflict.
- No visibility. Skill silently fails. Team doesn't know until user complains.

### Checklist

- [ ] Runbook is well-documented (each step is clear)
- [ ] Runbook is error-prone (manual steps, easy to forget)
- [ ] Skill implements key steps (not all—keep human in loop for validation)
- [ ] Skill is idempotent (safe to run twice)
- [ ] Skill logs actions taken
- [ ] Skill validates state before acting (no blindly executing)
- [ ] Skill has fallback to manual (escalates if something's wrong)
- [ ] Skill is tested in staging before production
