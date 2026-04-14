---
name: reviewing-failure-modes
description: Reviews how systems fail under dependency outages, partial writes, retries, and degraded states. Use when services coordinate remote calls, queues, or critical transactions.
when_to_use: failure mode, partial outage, degraded mode
allowed-tools: Read Grep
---

## Resilience Analysis and Mitigation

Failure is inevitable. The skill is anticipating failure modes (database down, API timeout, network partition) and designing systems that degrade gracefully.

### When to Use

- Designing new service or feature
- Resilience review before launch
- Incident post-mortem: "How do we survive this?"

### Decision Framework

1. **FMEA (Failure Mode and Effects Analysis).** List failure modes: database down, API timeout, cache miss. For each, design mitigation.
2. **Graceful degradation.** Feature depends on external API; API is slow? Show cached data, not error. User experience degrades; service doesn't fail.
3. **Circuit breaker pattern.** Calling slow external API? Stop calling after N failures. Return fallback. Retry periodically.
4. **Timeout and retry.** Request hangs = bad. Set timeout (5s); retry with exponential backoff (1s, 2s, 4s, 8s).
5. **Bulkhead isolation.** Payment service fails; shouldn't take down entire site. Isolate (separate thread pool, circuit breaker, queue).

### Anti-patterns to Avoid

- Assuming external services are reliable. They fail. Assume timeout.
- Cascading failures. Payment service down → order service down → web site down. Isolate and degrade gracefully.
- No fallback. API is slow; user gets error. Fallback to cached data.

### Checklist

- [ ] Failure modes are identified and documented
- [ ] Timeout is set for external requests
- [ ] Retry logic with exponential backoff
- [ ] Circuit breaker for external APIs
- [ ] Graceful degradation when dependency fails
- [ ] Fallback data or cached data is available
- [ ] Bulkhead isolation (separate resources per service)
- [ ] Test: kill database, API timeout, network partition; verify graceful degradation
