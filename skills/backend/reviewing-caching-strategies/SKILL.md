---
name: reviewing-caching-strategies
description: Reviews cache key design, invalidation strategy, TTL choices, layering, and stale-read risks. Use when introducing Redis, CDN, query, or application-level caching.
when_to_use: cache invalidation, redis, ttl
allowed-tools: Read Grep Bash
---

## Cache Invalidation and Performance

Caching is the cheapest optimization until it's wrong. The challenge: invalidation. Use appropriate strategies: TTL, write-through, event-based, or cache-aside. In Node.js/Python with Redis, the skill is knowing when to cache and when not to.

### When to Use

- Performance troubleshooting: DB queries are slow
- Designing read-heavy systems (dashboards, reports)
- Reducing load on expensive resources (external APIs, complex calculations)

### Decision Framework for Redis, Memcached, or In-Memory Cache

1. **Cache-Aside (Lazy Loaded).** Check cache; miss = load from DB, update cache, return. Simple, but cache miss is slow. Use for non-critical data.
2. **Write-Through.** Write to cache and DB together. Ensures cache is always fresh, but slightly slower writes.
3. **TTL (Time-To-Live) for simplicity.** Cache expires after N seconds. Reloads on next miss. Use for data that changes infrequently.
4. **Event-based invalidation for consistency.** Data changes → publish event → invalidate cache. Used in event-driven systems.
5. **Cache warming for hot data.** Pre-load cache at startup or on schedule. Avoids cold starts.

### Anti-patterns to Avoid

- Caching mutable objects in-process (Node.js or Python). Next deploy resets cache. Use external cache (Redis).
- Cache stampede: multiple processes miss cache simultaneously, all hit DB together. Use locks or probabilistic TTL.
- Stale cache due to no invalidation. Object updated in DB; cache still serves old data. Use TTL or event-based invalidation.
- Caching sensitive data without encryption. Cache breach = data breach.

### Checklist

- [ ] Cache strategy is defined (cache-aside, write-through, TTL, event-based)
- [ ] Cache misses are logged and monitored (hit ratio ≥70% is good)
- [ ] TTL is set appropriately (short for fast-changing data, long for static)
- [ ] Invalidation is triggered on writes (event, explicit, or TTL expiry)
- [ ] Cache is external (Redis, not in-memory in app process)
- [ ] Sensitive data in cache is encrypted or expires quickly
- [ ] Cache warming is implemented for hot data (pre-load at startup)
- [ ] Cache stampede is prevented (locks or probabilistic expiry)
- [ ] Test: update data in DB, verify cache is invalidated and reloaded
- [ ] Monitor: cache hit ratio, memory usage, eviction rate
