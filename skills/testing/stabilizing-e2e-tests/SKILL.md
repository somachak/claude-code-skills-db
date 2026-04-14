---
name: stabilizing-e2e-tests
description: Improves end-to-end tests by removing flakiness, clarifying waits, and aligning assertions with user-visible outcomes. Use when browser tests are brittle or slow.
when_to_use: playwright flake, cypress flake, e2e instability
allowed-tools: "Read Bash(npm run test*) Bash(pytest*)"
---

## End-to-End Testing Without Flakiness

E2E tests verify the full user flow (login → browse → checkout) using a real browser. They're slow and flaky if not designed well. The skill is fixing flakiness, managing state, and ensuring tests run reliably in CI.

### When to Use

- Critical user flows (login, payment, checkout)
- Post-deployment verification
- Regression detection

### Decision Framework for Playwright or Cypress

1. **Wait for state, not time.** `await page.click()` then `await page.waitForSelector('.success')`. Don't sleep. Flakiness is 95% impatience.
2. **Isolate test data.** Each test creates its own user, data. No shared state. Parallel tests don't interfere.
3. **Retry flaky steps.** Network hiccup = retry. `await retry(() => page.click('.button'))` with exponential backoff.
4. **Headless + headed for debugging.** CI runs headless (fast). Local dev runs headed (debug visually).
5. **Screenshots on failure.** Capture screenshot when test fails. Invaluable for debugging.

### Anti-patterns to Avoid

- Sleeping. `await page.goto(url); sleep(2000); expect()`. Flaky and slow. Wait for state instead.
- Shared test data. Test1 creates user; Test2 logs in with Test1's user. Tests can't run in parallel.
- No retry logic. Transient network error = test failure. Add retry wrapper.
- Sensitive data in tests. Hardcoded passwords. Use test accounts, not real production data.

### Checklist

- [ ] No sleep() statements; wait for state (waitForSelector, waitForNavigation)
- [ ] Test data is isolated per test (no shared users, products)
- [ ] Tests run in parallel without conflicts
- [ ] Retry logic for network-dependent steps
- [ ] Screenshots captured on failure
- [ ] Timeouts are reasonable (page navigation <10s)
- [ ] Run in headless mode in CI, headed locally
- [ ] Test sensitive flows (login, payment) without real credentials
- [ ] CI runs all tests; failure is loud and clear
