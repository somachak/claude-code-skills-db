---
name: improving-observability
description: Improves logging, metrics, tracing, and diagnostic context for faster debugging and healthier operations. Use when incidents are hard to diagnose or system behavior is opaque.
when_to_use: observability, tracing, structured logs
allowed-tools: Read Grep
---

## Logging, Metrics, and Tracing for Production Visibility

Observability = visibility into system behavior. Logging answers "what happened?", metrics answer "how much?", tracing answers "why is it slow?". The skill is collecting useful data and surfacing it quickly.

### When to Use

- Incident: need to understand what happened
- Performance: query is slow; why?
- Trends: error rate increasing; investigate

### Decision Framework for Prometheus, ELK, Datadog, or similar

1. **Structured logging.** JSON logs with context (user_id, request_id, service). Searchable and analyzable.
2. **Metrics for health.** Request latency, error rate, queue depth. Alerting on anomalies (error rate >1%).
3. **Distributed tracing.** Trace request across services (web → API → database). Find bottleneck (which service is slow?).
4. **Retention and cost.** Full logs for 7 days; sampled after. Metrics for 1 year. Tracing for 24 hours. Balance detail and cost.
5. **Dashboards for on-call.** Key metrics on one screen (error rate, latency, queue depth). On-call engineer can assess health in 30s.

### Anti-patterns to Avoid

- Logging everything. Storage cost explodes; noise drowns signal.
- No metrics. Logs tell you errors happened; metrics tell you the rate.
- No alerting. Errors occur; team doesn't know until user complains.

### Checklist

- [ ] Structured logging (JSON) with context (user_id, request_id)
- [ ] Key metrics are collected (latency, error rate, queue depth, resource usage)
- [ ] Alerts for critical metrics (error rate >X%, latency >Yms)
- [ ] Distributed tracing setup (request ID flows across services)
- [ ] Dashboards show health at a glance
- [ ] Log retention is set (7-30 days; archive older)
- [ ] On-call has clear procedure to investigate (runbook)
- [ ] Regular review of logs (errors, patterns); improve monitoring
