---
name: managing-feature-flag-lifecycle
description: Treats feature flags as a controlled lifecycle (design → ship → ramp → cleanup → archive) instead of throwaway if-statements. Use in Next.js / Node / FastAPI / Django apps when adding a flag, planning a progressive rollout, designing a kill switch, choosing between LaunchDarkly / GrowthBook / Statsig / Unleash / Flipt / homegrown, or auditing flag debt.
when_to_use: Adding, ramping, killing, or retiring a feature flag; auditing flag debt; choosing between LaunchDarkly, GrowthBook, Statsig, Unleash, Flipt, homegrown.
---

## Feature Flag Lifecycle

A flag is not an `if`-statement — it is a **lifecycle**: design → ship → ramp → cleanup → archive. Skip any step and you accumulate flag debt.

### The 4 Flag Types

| Type | Purpose | Lifespan | Cleanup trigger |
|---|---|---|---|
| **Release** | Hide unfinished work | days–weeks | 100% rollout reached |
| **Experiment** | A/B test variants | weeks | Experiment concludes |
| **Operational** | Kill switches, region toggles | indefinite | Tier-1 incident retired |
| **Permission** | Per-customer / per-plan gating | indefinite | Move to entitlements service |

### Ring-Based Rollout

```
Ring 0  internal       1%   24h
Ring 1  power users    5%   48h
Ring 2  small cohort  20%   72h
Ring 3  half pop      50%   72h
Ring 4  everyone     100%   ─
```
Promote only if error rate within ±10%, p95 latency not >20% worse, on-call ack rate steady.

### Provider Picker

- **LaunchDarkly** — enterprise SDKs, audit logs. Pick for SOC2/customer-rule targeting.
- **GrowthBook** — OSS, strong experiment stats. Pick when experimentation is primary.
- **Statsig** — generous free tier, Pulse analytics. Pick for flags+analytics in one pane.
- **Unleash / Flipt** — fully self-hosted. Pick for data residency / air-gap.
- **Homegrown config table** — only fine for ≤10 flags total, no experimentation.

### Kill-Switch Requirements

1. Single env var / remote-config key disables path in <60s.
2. Documented owner and Slack channel.
3. Smoke test that the kill switch actually kills the path.
4. Fallback behaviour is safe and known.

### Stack-Specific Notes

- **Next.js** — Read flags in a Server Component or at the edge in middleware. Never read client-side without a stable user id.
- **FastAPI / Django** — Resolve in a request-scoped dependency / middleware; cache per-request, not per-call.
- **Node services** — Use streaming SDK update mode so a kill flip propagates in seconds.

### Anti-Patterns

- `if (flag)` and `if (!flag)` both untested — one branch ships, one rots.
- Same flag read in 30 places — centralise in a typed wrapper.
- Long-lived release flag — set expiry at creation; >90 days at 100% is debt.

### Cleanup Checklist

- [ ] Flag type classified.
- [ ] Rollout ring plan documented before flip.
- [ ] Kill switch verified in staging.
- [ ] Owner + Slack channel listed.
- [ ] Cleanup ticket auto-filed N days after 100%.
