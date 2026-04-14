---
name: building-background-jobs
description: Designs reliable background jobs, retry logic, scheduling strategy, idempotency, and failure handling. Use when adding workers, task queues, cron-style jobs, or async processing pipelines.
when_to_use: queue worker, retry logic, idempotency
allowed-tools: Read Grep Bash
---

## Async Jobs, Workers, and Queues

Not all work happens in a request-response cycle. Sending emails, generating reports, processing files: these belong in background jobs. Use job queues (Bull/BullMQ in Node, Celery in Python) to decouple work from HTTP responses.

### When to Use

- Long-running tasks (report generation, file processing, ML pipelines)
- Retryable work (email delivery, webhooks, data syncs)
- Scheduled work (cron jobs, daily reports, cleanup)
- Rate-limited external APIs (YouTube uploads, Slack posts)

### Decision Framework for Node.js (Bull/BullMQ) or Python (Celery/APScheduler)

1. **Queue name = job type.** Separate `email-queue`, `report-queue`, `cleanup-queue`. Monitor each independently.
2. **Job data is payload only.** Pass IDs, not huge objects. Job fetches fresh data when it runs (safer, smaller queue).
3. **Exponential backoff for retries.** Fail once, retry in 1s; fail again, retry in 2s, then 4s, then 8s (max). Avoids thundering herd.
4. **Idempotency is required.** Same job running twice should be safe. Use idempotency keys or check "already done" state before side effects.
5. **Monitor and alert.** Track queue depth, failure rate, processing time. Dead-letter queue for jobs that fail N times.

### Anti-patterns to Avoid

- Spawning child processes or threads in request handlers instead of queueing. Kills request timeout and resets on deploy.
- Serializing huge objects into job payload. Pass an ID; fetch fresh data in the job.
- No retry logic. Fire-and-forget emails = lost emails. Use exponential backoff.
- Mixing sync and async work in one job. A job should be idempotent and restartable.
- Not logging job state. No way to debug a failed job.

### Checklist

- [ ] Jobs are queued, not spawned in request handlers
- [ ] Job payload is small (IDs only); data is fetched inside the job
- [ ] Retry logic with exponential backoff is implemented
- [ ] Each job type has its own queue and worker
- [ ] Dead-letter queue captures jobs that fail N times
- [ ] Job success and failure are logged with context
- [ ] Idempotency: same job running twice has no harmful side effects
- [ ] Scheduled jobs (cron) have clear purpose and SLA
- [ ] Queue monitoring is set up (depth, failure rate, processing time)
- [ ] Test: run job, run again—verify it's safe
