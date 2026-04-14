---
name: reproducing-bugs-from-logs
description: Turns logs, traces, and error reports into concrete reproduction steps and regression tests. Use when investigating production failures, support tickets, or intermittent defects.
when_to_use: reproduce bug, logs to test, incident reproduction
allowed-tools: "Read Bash(npm run test*) Bash(pytest*)"
---

## Log Analysis and Error Reproduction

Production bugs are hard to debug without logs. The skill is structuring logs so you can reproduce (or understand) issues from error traces, request IDs, and user context.

### When to Use

- Production incident: user reports "checkout failed"
- Error spike: hundreds of 500s, need to understand why
- Flaky issue: happens once a week, need to reproduce

### Decision Framework for Structured Logging (Winston, Pino, Python logging)

1. **Structured logging, not printf.** `logger.error({ userId, orderId, error: err.message, stack: err.stack })` → JSON → searchable. Not "Error occurred".
2. **Request IDs link events.** Every request gets unique ID (UUID). All logs for that request include ID. Trace full request → database → API call → response.
3. **Error context is crucial.** Don't just log error message. Include variables at time of error (user ID, order ID, payment status). Why did it fail, not just that it failed.
4. **Log levels are meaningful.** DEBUG (development), INFO (expected events), WARN (recoverable problems), ERROR (failures), FATAL (process crash).
5. **Sampling for high-volume logs.** If logging every request and you're 1M req/day, storage is expensive. Sample: log 1 in 100 requests, all errors.

### Anti-patterns to Avoid

- Unstructured logs. "Error occurred" with no context. Can't reproduce or understand.
- No request ID. Logs from user request mixed with logs from other requests. Can't follow request.
- Logging sensitive data. Passwords, credit cards in logs = breach when logs are leaked.
- No timestamp or timezone. When did error occur? Hard to correlate with other events.

### Checklist

- [ ] Logs are structured (JSON), not printf format
- [ ] Every request has unique ID (UUID); included in all logs
- [ ] Error logs include context (user ID, resource ID, variables at time of error)
- [ ] Log levels are used correctly (DEBUG, INFO, WARN, ERROR, FATAL)
- [ ] No sensitive data logged (passwords, credit cards, PII)
- [ ] Timestamp and timezone are included
- [ ] Error stack traces are logged in full
- [ ] Log aggregation tool (ELK, DataDog) is set up; searchable by request ID
- [ ] Test: generate error, search logs by request ID, can reproduce path
