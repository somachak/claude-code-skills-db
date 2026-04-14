---
name: handling-webhooks
description: Builds and reviews webhook consumers for signature verification, retries, deduplication, ordering issues, and replay safety. Use when integrating payment, messaging, or external event providers.
when_to_use: webhook, signature verification, replay attack
allowed-tools: Read Grep Bash
---

## Receiving and Processing Webhooks Securely

Webhooks are callbacks: external services POST to your endpoint when an event occurs. The challenge: verifying the sender, handling retries, idempotency, and failure scenarios.

### When to Use

- Integrating Stripe, GitHub, Slack, or other event sources
- Designing an event notification system for your own platform
- Debugging webhook delivery failures or replay scenarios

### Decision Framework for Express/FastAPI + Node.js or Python

1. **Verify webhook signature.** Stripe, GitHub, etc. send a signature (HMAC-SHA256). Verify it before trusting the payload. Prevents spoofing.
2. **Idempotency is essential.** Webhook sent twice? Process it safely twice. Use an idempotency key (event ID) to detect duplicates.
3. **Respond 2xx immediately.** Queue the work; don't block the sender waiting for processing. Respond 200 OK, then process asynchronously.
4. **Handle retries gracefully.** Sender will retry. Exponential backoff, dead-letter queue, and manual replay tools.
5. **Log and monitor.** Track webhook URL, signature verification, processing success, failures. Set up alerts for failure spikes.

### Anti-patterns to Avoid

- Not verifying signatures. Attacker posts to your webhook endpoint posing as Stripe.
- Synchronous processing. Webhook sender times out waiting for you to finish work.
- Storing webhook payloads without verification. Unverified payload = possible poisoned state.
- No logging. Can't debug delivery failures or replay scenarios.
- Tight coupling to webhook provider's schema. Schema changes break processing. Validate and normalize early.

### Checklist

- [ ] Webhook endpoint validates HMAC signature before processing
- [ ] Payload is queued for async processing (don't block the sender)
- [ ] Response is 200 OK immediately; processing happens in background job
- [ ] Idempotency key (event ID) prevents double-processing
- [ ] Failed processing is retried with exponential backoff
- [ ] Webhook logs include timestamp, signature validation result, success/failure
- [ ] Manual replay tool exists for re-processing missed or failed webhooks
- [ ] Monitoring/alerting on webhook failure rate and latency
- [ ] Test: send webhook twice with same event ID; verify it's only processed once
- [ ] Test: send webhook from attacker with wrong signature; verify it's rejected
