---
name: validating-etl-pipelines
description: Validates ETL and ELT pipelines for freshness, schema drift, lineage breaks, duplication, and reconciliation errors. Use when building ingestion jobs, warehouse transforms, or sync systems.
when_to_use: etl validation, schema drift, pipeline freshness
allowed-tools: Read Grep
---

## Data Pipeline Quality and Observability

ETL (Extract, Transform, Load) pipelines ingest data from sources, transform, and load to warehouse or database. Quality is paramount: bad data → bad decisions. The skill is validation, error handling, and recovery.

### When to Use

- Building a data pipeline (analytics, reporting, sync)
- Pipeline is failing or data is wrong
- Scaling pipeline to handle more sources or volume

### Decision Framework for Apache Airflow, dbt, or custom Python/Node.js

1. **Validate schema at every stage.** Source data, after extraction, after transformation. Reject invalid rows early; don't propagate garbage.
2. **Idempotency is essential.** Same source data processed twice should result in same warehouse state. Use upsert (INSERT OR UPDATE) or deduplication.
3. **Monitor data quality.** Record counts, schema drift, freshness. Alert on failures.
4. **Backfill is common.** Pipeline fails for a day; backfill missing data. Pipeline must support rerunning for past dates.
5. **Error handling is non-trivial.** Partial failure: 999 rows loaded, 1 fails. Quarantine failed rows; notify; resume.

### Anti-patterns to Avoid

- No validation. Data loaded as-is; garbage in, garbage out.
- Non-idempotent pipelines. Reruns produce duplicates or inconsistencies.
- No monitoring. Pipeline fails silently; stale data in warehouse for weeks.
- Tight coupling between stages. Transformation depends on specific source format; breaks on schema change.

### Checklist

- [ ] Source data schema is validated (required fields, types, ranges)
- [ ] Transformation rules are tested on sample data
- [ ] Pipeline is idempotent (can rerun; result is same)
- [ ] Failed rows are logged and quarantined (not lost)
- [ ] Record count validation (source count == loaded count after transformation)
- [ ] Freshness monitoring (alert if data >24 hours old)
- [ ] Backfill capability (can reprocess past dates)
- [ ] Data quality metrics are tracked (completeness, uniqueness, timeliness)
- [ ] Test: run pipeline twice; verify same warehouse state
