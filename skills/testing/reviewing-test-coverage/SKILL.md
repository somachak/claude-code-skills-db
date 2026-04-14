---
name: reviewing-test-coverage
description: Reviews what is not tested and prioritizes the highest-risk missing scenarios. Use when shipping new code, after large refactors, or after incidents that revealed blind spots.
when_to_use: coverage gaps, missing tests, risk-based testing
allowed-tools: "Read Bash(npm run test*) Bash(pytest*)"
---

## Coverage Metrics and Gap Analysis

Coverage (% of code executed by tests) is a metric, not a goal. 80% coverage is useful; 100% is often not. The skill is interpreting coverage reports, identifying gaps, and prioritizing.

### When to Use

- Code review: "Is this change tested?"
- Audit: overall coverage %, trends
- Risk assessment: untested critical paths

### Decision Framework for Codecov, Istanbul, Pytest, or Coverage.py

1. **Focus on critical paths.** Authentication, payments, data validation: high priority. UI polish: lower priority.
2. **Branch coverage > line coverage.** Line coverage misses branches. "if (x) { a() } else { b() }" with only "if" branch covered = gap. Use branch coverage.
3. **Integration tests count.** Unit test doesn't have to cover every line if integration tests do.
4. **Untested is technical debt.** 80% coverage + untested critical path = risk. 100% coverage + untested edge case = less risk.
5. **Coverage trends matter.** Coverage declined 5% last month = bad. Investigate and require tests for new code.

### Anti-patterns to Avoid

- Obsessing over 100% coverage. Diminishing returns; time better spent on risky features.
- Ignoring low-coverage files. If something's important, it should be tested.
- Generating tests only to hit coverage targets. Meaningless tests.

### Checklist

- [ ] Coverage report generated and tracked (Codecov)
- [ ] Overall coverage ≥80%
- [ ] Critical paths (auth, payments, validation) have ≥90% coverage
- [ ] Branch coverage is reported (not just line coverage)
- [ ] Low-coverage files are reviewed (untested critical code)
- [ ] Coverage trends are monitored (month-over-month)
- [ ] New code requires tests before merge
- [ ] Flaky tests are removed or fixed (they mask real issues)
