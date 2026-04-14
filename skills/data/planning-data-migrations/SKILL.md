---
name: planning-data-migrations
description: Plans safe schema and data migrations with backfills, rollout sequencing, rollback paths, and runtime compatibility checks. Use when changing live data models or moving data between stores.
when_to_use: migration plan, backfill, zero downtime migration
allowed-tools: Read Grep
---

## Safe, Reversible Database Changes

Migrations change production schema without downtime. The skill is writing safe migrations, testing them, and coordinating with application deploys to avoid conflicts.

### When to Use

- Adding, removing, or renaming columns
- Changing column types or constraints
- Creating or dropping indexes
- Large data backfills

### Decision Framework for Knex, Alembic, or Django Migrations

1. **Migrations must be reversible.** UP (add column), DOWN (remove column). Test both directions.
2. **Backfill data in separate migration.** Add column (NOT NULL): add column (nullable), backfill, add constraint. Avoids long locks.
3. **Coordinate with app deploy.** If removing column, app must stop using it first. Deploy app → remove column (next deploy).
4. **Large tables need special care.** Add index on 1B-row table = hours of locking. Use CONCURRENTLY (PostgreSQL) or online DDL (MySQL 8+).
5. **Test migrations on staging first.** Run migration, verify schema, measure downtime, revert. Repeat on production.

### Anti-patterns to Avoid

- No rollback testing. Assume DOWN works? It doesn't. Test both directions.
- Data loss migration without backup. Always backup before major migrations.
- Long-running migrations during peak traffic. Schedule for maintenance window or use online DDL.
- Mixing structural and data migrations. Keep them separate for clarity and rollback.

### Checklist

- [ ] Migration is reversible (UP and DOWN both tested)
- [ ] Migration doesn't remove data without backup
- [ ] Large data changes use backfill migration (separate step)
- [ ] Adds constraints only after data is backfilled
- [ ] Tests on staging environment first (full schema, data size, downtime)
- [ ] Downtime is acceptable or uses online DDL (CONCURRENTLY, MySQL 8+)
- [ ] Rollback procedure is documented and tested
- [ ] Coordination with app deploy: app doesn't use removed/renamed columns
