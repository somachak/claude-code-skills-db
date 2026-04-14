---
name: validating-backup-and-restore
description: Validates backup scope, recovery steps, restore drills, and data integrity assumptions. Use when services store critical operational or customer data.
when_to_use: backup restore, recovery drill, rpo rto
allowed-tools: Read Grep
---

## Data Protection and Disaster Recovery

Backups are only useful if you can restore them. The skill is testing restore procedures, knowing RTO (Recovery Time Objective) and RPO (Recovery Point Objective), and ensuring backups are encrypted and stored safely.

### When to Use

- Launch of new service
- Quarterly backup testing
- Incident: data corruption, need to restore

### Decision Framework for Backup Strategy

1. **Automated daily backups.** Don't rely on manual dumps. Schedule via cron or managed service.
2. **Multiple backup locations.** Local, offsite, cloud. If one is compromised, others survive.
3. **RTO and RPO are explicit.** RTO: time to restore (target: <1 hour for critical data). RPO: data loss (target: <1 hour). Affects backup frequency and retention.
4. **Restore testing, not just backups.** Backup is worthless if restore fails. Test monthly: restore to staging, verify data integrity.
5. **Encryption at rest and in transit.** Backup is a juicy target. Encrypt with key managed separately from data.

### Anti-patterns to Avoid

- No backups. Too expensive or "we won't need it." Hardware fails.
- Backups not tested. "We have backups" until restore fails.
- Single backup location. Compromised = all gone.
- No encryption. Backup leaked = data breach.

### Checklist

- [ ] Automated daily backups (database, files, configs)
- [ ] Backups are stored in multiple locations (local, cloud, offsite)
- [ ] Backups are encrypted (AES-256) with separate key management
- [ ] RTO and RPO are defined and achievable
- [ ] Restore procedure is documented and tested
- [ ] Monthly restore test to staging; verify data integrity
- [ ] Retention policy is clear (keep 30 days, archive old)
- [ ] Monitoring: backup success/failure, storage usage
