---
name: running-chaos-experiments
description: "Plans and runs disciplined chaos experiments against Node, FastAPI, and Django services: defining steady state, sizing blast radius, choosing fault injection tools, and writing the abort criteria before the experiment starts. Use when preparing a GameDay, validating a new failover path, or stress-testing a freshly deployed service before peak traffic."
when_to_use: Before a GameDay, post-launch resilience check, or validating a new failover path under controlled fault injection.
---

## Chaos Experiments for Production Web Services

Chaos engineering only buys you something if the experiment is designed with falsifiable hypotheses and bounded blast radius. Random pod kills aren't an experiment — they're outages with extra steps.

### When to Use

- You shipped a new failover path (read replica, queue retry, circuit breaker) and want to prove it works before traffic does
- A FastAPI or Express service depends on a third-party API and you don't know how it behaves under that dependency's latency
- A retro called out a failure mode no one had simulated (e.g. "we'd never tested losing the cache") and you want to retire that risk
- Pre-launch capacity planning — running a controlled experiment before Black Friday beats a real one during it

### When NOT to Use

- The system has known unfixed bugs — fix those first, chaos will just reproduce them expensively
- Observability is missing — you can't read the result of an experiment you can't measure
- No on-call rotation can respond if the experiment escapes the blast radius

### Decision Framework

1. **Steady state first.** Write down the metric that defines "healthy" before injecting anything — p95 latency, success rate, queue depth. The experiment is a comparison, not an observation.
2. **Hypothesis is falsifiable.** "The checkout API stays under 800ms p95 when the primary database loses 100ms of latency" — measurable, time-boxed, and the experiment can disprove it.
3. **Blast radius is the smallest set of users that lets you learn.** Start in staging with synthetic traffic. Graduate to one canary pod with 1% real traffic. Only run on full production traffic when the first two passed.
4. **Abort criteria written before start.** Two SLOs and a kill switch: error rate breaches X, latency breaches Y, or any P1 alert fires → roll back. This goes in the experiment doc, not the heads of the people running it.
5. **Pick the right tool for the failure.** Network latency → Toxiproxy or `tc netem`. Pod kill → Chaos Mesh or `kubectl delete pod`. Region outage → only with leadership sign-off and a customer comms plan.

### Anti-patterns

- Running chaos without observability — you'll only learn that you can't see anything
- "Surprise GameDay" with no warning — on-call burns out, and the lesson is that chaos = ambush
- Rolling experiments forward when steady state drifts — pause, reset, then continue
- Treating green dashboards as a pass — also check error budget burn and downstream queue depth

### Worked Example — payment service GameDay

```
Hypothesis: orders/checkout p95 stays under 800ms when Stripe API responds at +500ms latency.
Steady state: 99.5% checkout success, 600ms p95, queue depth <50.
Blast radius: 5% of traffic via Envoy weight, US-East region only, 30 minutes.
Fault: Toxiproxy adds 500ms latency to api.stripe.com (sidecar in canary pods).
Abort: success <99%, p95 >900ms, or on-call pages → revert Envoy weight to 0%.
Observation: queue retries doubled within 8 minutes, breached abort threshold, reverted.
Finding: retry backoff was 100ms (configured) but Stripe's recommended backoff is 1s+jitter — fix scheduled.
```

### Validation Loop

- [ ] Steady-state SLOs measured for 24h prior to experiment
- [ ] Abort criteria documented and the kill-switch tested in staging
- [ ] Comms posted in #incidents 15 minutes before start, again at start, again at end
- [ ] Findings filed within 48h (bugs, dashboard gaps, missing alerts)
- [ ] Each finding has an owner and a deadline before the next experiment
