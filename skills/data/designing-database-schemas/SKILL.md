---
name: designing-database-schemas
description: Designs relational schemas, keys, constraints, and normalization tradeoffs for operational systems. Use when creating new tables, domain models, or storage-backed product features.
when_to_use: database schema, table design, foreign keys
allowed-tools: Read Grep
---

## Normalization, Constraints, and Access Patterns

Database schema is architecture. Good schema enables fast queries, prevents data anomalies, and scales. Bad schema requires complex application logic and causes corruption. The skill is normalization (3NF or BCNF), constraint design, and access pattern optimization.

### When to Use

- Designing a new database or table
- Reviewing schema for normalization and performance
- Refactoring due to data anomalies or slow queries

### Decision Framework for PostgreSQL/MySQL + Node.js/Python

1. **Normalize to 3NF by default.** Eliminate redundancy: no repeated columns (first names across rows), no transitive dependencies (city shouldn't depend on state via zipcode).
2. **Constraints enforce data integrity.** NOT NULL, UNIQUE, FOREIGN KEY, CHECK. Let the database reject invalid states; don't rely on application logic.
3. **Primary key is essential.** Every table needs a unique identifier. Use auto-incrementing INT or UUID. Avoid composite keys when a surrogate works.
4. **Indexes for access patterns.** Profile the queries; index the columns used in WHERE, JOIN, ORDER BY. Too many indexes slow writes; too few slow reads.
5. **Denormalize for performance, not by default.** Sometimes a user's email is stored on Order for fast lookups, avoiding a JOIN. Do it only when profiling shows it's worth it.

### Anti-patterns to Avoid

- Storing JSON blobs instead of normalized tables. Queries become slow and unmaintainable.
- No constraints. Application enforces NOT NULL, UNIQUE, FOREIGN KEY? That's fragile.
- Composite primary keys instead of surrogates. Difficult to reference, slow to index.
- Over-indexing. Every column is indexed = slow inserts, large storage.

### Checklist

- [ ] Schema is normalized to 3NF (no redundancy, no transitive dependencies)
- [ ] Every table has a primary key (surrogate ID preferred)
- [ ] Constraints enforce data integrity (NOT NULL, UNIQUE, FOREIGN KEY, CHECK)
- [ ] Indexes exist for common access patterns (WHERE, JOIN, ORDER BY columns)
- [ ] Large tables have partitioning strategy (if >100GB or >1B rows)
- [ ] Data types are appropriate (VARCHAR(255) vs TEXT, INT vs BIGINT)
- [ ] Migrations are version-controlled and reversible
- [ ] Test: insert invalid data (violate constraint); verify DB rejects it
