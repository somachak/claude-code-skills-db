---
name: generating-unit-tests
description: Generates focused unit tests around branches, edge cases, and regressions without overfitting to implementation details. Use when extending logic, fixing bugs, or improving confidence in isolated modules.
when_to_use: unit tests, edge case tests, regression test
allowed-tools: "Read Bash(npm run test*) Bash(pytest*)"
---

## Unit Test Design and Coverage

Unit tests verify single functions in isolation. The skill is writing fast, focused tests that catch regressions without being brittle.

### When to Use

- Writing new functions or components
- Reviewing untested code
- Coverage audit (target >80%)

### Decision Framework for Jest, Pytest, or Vitest

1. **One assertion per test.** Test name says what it verifies. test('sum returns 5 when given 2 and 3'). Multiple assertions = one fails, rest skipped.
2. **Mock external dependencies.** Database, API, filesystem: mock them. Unit test should not hit network or disk.
3. **Fixtures for setup.** beforeEach initializes test data. Cleaner than inline setup.
4. **Coverage, not completeness.** 80% coverage catches most bugs. 100% is tedious; diminishing returns. Focus on complex logic, edge cases.
5. **Test behavior, not implementation.** Test that sum(2, 3) === 5, not the internal algorithm.

### Anti-patterns to Avoid

- Testing private implementation details. If method is private, test via public API.
- No mocks. Unit test calls real database = slow, flaky.
- Multiple assertions per test. One fails, others skip.
- Brittle assertions. test('array has 3 items') fails if data changes. Prefer assertions on structure.

### Checklist

- [ ] One assertion per test (or logically related assertions)
- [ ] Mocks for I/O (database, API, filesystem)
- [ ] Fixtures for common setup
- [ ] Test name describes what it verifies
- [ ] Coverage is ≥80% (Codecov, istanbul)
- [ ] Flaky tests are investigated and fixed
- [ ] Test runs in <1s (not waiting on mocks)
- [ ] Edge cases are tested (null, empty, very large values)
