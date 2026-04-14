---
name: designing-integration-tests
description: Designs integration tests around service contracts, persistence, side effects, and environment setup. Use when changes cross module, network, storage, or framework boundaries.
when_to_use: integration test, service contract, testcontainers
allowed-tools: "Read Bash(npm run test*) Bash(pytest*)"
---

## Multi-Unit Testing and Contract Validation

Integration tests verify multiple units working together (API endpoint + database, authentication + authorization). The skill is setting up test databases, coordinating state, and validating contracts.

### When to Use

- Testing API endpoints (request → database → response)
- Verifying database transactions and constraints
- Testing background jobs and async flows

### Decision Framework for Jest, Pytest, or testcontainers

1. **Test database is real database.** Use testcontainers (Docker) to spin up PostgreSQL, Redis, etc. for each test suite. Clean and fast.
2. **Fixtures seed data.** beforeAll seeds users, products; afterAll truncates. Reproducible state.
3. **Test API via HTTP client.** Don't call app.get() directly. Use supertest (Node) or httpx (Python). Tests the real request cycle.
4. **Assertions on side effects.** API creates invoice → assert it's in database, email is queued, webhook is sent.
5. **Timeouts are real.** Integration tests are slower; adjust timeouts. 5s vs. 100ms for unit.

### Anti-patterns to Avoid

- Sharing database across tests. One test's data leaks to others.
- Mocking the database. Defeats purpose of integration test.
- Non-deterministic tests. Random data, time-dependent logic. Tests pass once, fail next time.
- Not cleaning up. Test creates file or database entry; next test fails due to leftover state.

### Checklist

- [ ] Test database is isolated per test suite (Docker testcontainers)
- [ ] Fixtures seed known data (beforeAll/afterAll)
- [ ] API is tested via HTTP, not direct app.get()
- [ ] Assertions verify database state after request
- [ ] Background jobs or async flows are awaited
- [ ] Tests are deterministic (no random data, fixed timestamps)
- [ ] Cleanup is automatic (afterAll truncates database)
- [ ] Timeouts are appropriate for integration (5s, not 100ms)
