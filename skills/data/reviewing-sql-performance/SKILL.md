---
name: reviewing-sql-performance
description: Reviews SQL queries for plan quality, indexing opportunities, cardinality traps, and unnecessary scans. Use when queries slow down APIs, jobs, dashboards, or analytics pipelines.
when_to_use: slow query, sql tuning, index
allowed-tools: Read Grep
---

## Query Optimization and Execution Plans

Slow queries are the #1 database performance killer. The skill is reading execution plans, identifying index misses, and rewriting queries to be efficient.

### When to Use

- Query runs in >100ms; need to optimize
- Database CPU or disk I/O is high
- Analyzing slow query logs
- Indexing strategy for a new feature

### Decision Framework for PostgreSQL/MySQL

1. **EXPLAIN PLAN is your friend.** Run EXPLAIN ANALYZE SELECT ... to see execution plan. Sequential scans = missing index. Nested loops with high loop count = missing JOIN condition.
2. **Index selectivity matters.** Index on is_active (two values) has low selectivity; index on user_id (many values) has high selectivity. Optimize high-selectivity columns.
3. **JOIN order affects performance.** Smaller table first, then join to larger. Database optimizer usually gets this right, but not always.
4. **Aggregation can be expensive.** COUNT(*) is slow on 1B-row table without index. Use approximate COUNT (APPROX_COUNT) if exact is unnecessary.
5. **Pagination without offset.** `OFFSET 1000 LIMIT 10` scans 1000 rows. Use keyset pagination (WHERE id > last_id LIMIT 10) instead.

### Anti-patterns to Avoid

- N+1 queries: select user, then for each user select posts. Use JOIN or batch load.
- Full table scans. Missing index on WHERE column = sequential scan on 1M rows.
- Sorting in application code. Offload ORDER BY to database; it uses indexes.
- Subqueries in SELECT. `SELECT id, (SELECT COUNT...) FROM users` = loop over all users + subquery. Use JOIN + GROUP BY.

### Checklist

- [ ] EXPLAIN ANALYZE shows index scans, not sequential scans (for large tables)
- [ ] No N+1 queries; use JOIN or batch load
- [ ] Slow query log is configured; queries >100ms are logged
- [ ] Indexes exist for WHERE, JOIN, and ORDER BY columns
- [ ] Query rewrite: replace subqueries with JOINs
- [ ] Pagination uses keyset, not offset
- [ ] Test: monitor query time before and after optimization; verify improvement
