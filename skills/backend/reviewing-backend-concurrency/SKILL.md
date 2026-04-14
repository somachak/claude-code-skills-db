---
name: reviewing-backend-concurrency
description: Reviews concurrent backend code for race conditions, deadlocks, ordering bugs, lock contention, and inconsistent side effects. Use when services coordinate shared state, workers, or high-throughput workloads.
when_to_use: race condition, deadlock, concurrency bug
allowed-tools: Read Grep Bash
---

## Concurrency Patterns and Data Races

Concurrency is hard: race conditions, deadlocks, and data corruption lurk in multi-threaded or async code. In Node.js (async/await), Python (asyncio, threading), and databases, the skill is understanding isolation levels, locks, and atomic operations.

### When to Use

- Reviewing multi-threaded or async code for race conditions
- Designing concurrent request handling (thousands of simultaneous users)
- Analyzing database deadlocks or lock contention
- Ensuring atomicity in critical sections (payments, inventory, user creation)

### Decision Framework for Node.js (async/await) or Python (asyncio)

1. **Single-threaded concurrency (async/await) scales better than threads.** Node.js and Python asyncio avoid OS thread overhead. Use threads only for CPU-bound work (Node.js worker threads, Python multiprocessing).
2. **Database transactions ensure atomicity.** Wrap multi-step operations (debit account A, credit account B) in a transaction with appropriate isolation level (READ COMMITTED for most cases, SERIALIZABLE for financial).
3. **Optimistic locking for high-concurrency scenarios.** Instead of row locks, use a version field (optimistic_lock_version). Retry on conflict.
4. **Message queues decouple writes.** If many processes write to the same resource, use a queue to serialize writes.
5. **Immutable state is safer.** Immutable objects don't suffer race conditions. In mutable languages, use immutable data structures or functional patterns.

### Anti-patterns to Avoid

- Race condition: read-check-write without a lock. `if (user.balance >= amount) { user.balance -= amount; }` is unsafe in concurrent code.
- Deadlock: two processes lock A, then wait for lock B, while the other has B and waits for A. Use consistent lock ordering.
- No isolation: database reads uncommitted changes from other transactions. Use appropriate isolation level.
- Unbounded concurrency. If you allow 10,000 concurrent requests, your database connection pool is exhausted. Use a queue or backpressure.

### Checklist

- [ ] Critical sections (payments, inventory) are wrapped in database transactions
- [ ] Transaction isolation level matches the need (READ COMMITTED is default; use SERIALIZABLE for high-value operations)
- [ ] Optimistic or pessimistic locking is used where contention is expected
- [ ] No read-check-write patterns without locks
- [ ] Async code doesn't share mutable state without synchronization
- [ ] Concurrency testing: multiple processes write same resource; verify no data loss
- [ ] Deadlock testing: confirm lock ordering is consistent, no circular dependencies
- [ ] Monitor database lock wait times; alert on spikes
- [ ] Backpressure is implemented (queue depth, connection pool saturation)
