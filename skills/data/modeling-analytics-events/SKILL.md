---
name: modeling-analytics-events
description: Models analytics events, naming conventions, user properties, and event contracts for trustworthy product analysis. Use when adding instrumentation to frontend or backend product flows.
when_to_use: tracking plan, analytics events, event naming
allowed-tools: Read Grep
---

## Event Schema, Collection, and Attribution

Analytics events tell you how users interact with your app. Good event schema enables product insights; bad schema is noise. The skill is designing event payloads, sampling strategies, and attribution models.

### When to Use

- Designing analytics for a new feature or product
- Auditing event quality (too noisy, missing context)
- Attribution and user journey tracking

### Decision Framework for Analytics Platform (Mixpanel, Amplitude, custom)

1. **Event schema must be versioned and validated.** Define event name, required properties (user_id, timestamp), optional properties (metadata). Use JSON Schema or similar.
2. **User context is critical.** Every event includes user_id, session_id, timestamp, OS, browser, country. Context enables segmentation.
3. **Avoid event explosion.** Don't emit PageView for every page. Use a standardized schema (page_title, page_category) instead of per-page events.
4. **Sampling for scale.** If events are 1M/day, sample to 10%; store full resolution for top features. Instrumentation cost vs. insight tradeoff.
5. **Attribution model for multi-touch.** First-touch, last-touch, or multi-touch? Choose early; it affects ROI calculations and budget allocation.

### Anti-patterns to Avoid

- No event schema. "Send whatever properties feel useful." Result: inconsistent data, hard to analyze.
- Event explosion. One event per button click, per input change. Massive cardinality; storage blows up.
- No user context. Events are orphaned; can't attribute to users.
- Sampling not documented. Analysis assumes full resolution; results are wrong.

### Checklist

- [ ] Event schema is defined and versioned (JSON Schema or similar)
- [ ] Every event includes user_id, session_id, timestamp, OS, browser
- [ ] Event names follow naming convention (object_action: user_clicked, invoice_paid)
- [ ] Property names are consistent (user_id, not userId or uid)
- [ ] Sampling strategy is defined and documented
- [ ] PII is not logged (no email, password, credit card)
- [ ] Event delivery is reliable (retry, queue, confirmation)
- [ ] Analytics events are validated on client or server (schema check)
- [ ] Monthly audit: unused events removed, schema validated
