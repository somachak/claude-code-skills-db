---
name: designing-graphql-apis
description: Designs GraphQL schemas, resolver boundaries, batching, and authorization rules. Use when building graphs, federated services, or resolver-heavy integrations.
when_to_use: graphql schema, resolver performance, n+1
allowed-tools: Read Grep Bash
---

## GraphQL Schema & Query Optimization

GraphQL gives clients exactly what they ask for. The trade-off: schema design is critical, and without discipline, N+1 queries and overfetching happen. In Node.js (Apollo), Python (Strawberry, Graphene), and TypeScript, the skill is schema organization, resolvers, and preventing common pitfalls.

### When to Use

- Designing a new GraphQL schema or endpoint
- Optimizing slow GraphQL queries or field resolvers
- Reviewing schema for naming, nesting, and performance
- Migrating from REST or adding a GraphQL layer

### Decision Framework for Node.js/TypeScript + Apollo or Python Strawberry

1. **Flat schema, nested queries.** Don't nest types deeply (User > Post > Comment > Author > Profile). Query shape allows nesting; schema stays flat.
2. **Single responsibility per field.** A User.posts field should only return posts, not posts with comments and comments with authors all loaded. Let the client query what it needs.
3. **Resolver should be fast or cached.** If a resolver makes a DB call per field, you have N+1. Use dataloader (Node) or select_related/prefetch_related (Django) to batch queries.
4. **Union and Interface for polymorphism.** Use them sparingly; they add complexity. A `SearchResult` union of User | Post | Comment makes sense; nesting unions inside unions doesn't.
5. **Subscription and mutation design.** Mutations return the mutated object (plus errors) so the client can update cache. Subscriptions push changes to subscribed clients.

### Anti-patterns to Avoid

- Deep nesting: query User > Posts > Comments > Replies > Author > Profile. Makes schema complex and resolution slow.
- N+1 resolver problem: User field loads user, then each Post resolver loads the User again. Use dataloader.
- Over-nesting arguments: `user(id: ID!, filter: Filter!, sort: Sort!, pagination: Pagination!)`. Use input types.
- No error handling in resolvers. Exceptions propagate; use a consistent error type or error wrapper.
- Serving sensitive data in schema. An unauthorized user shouldn't be able to query admin fields. Use resolver middleware.

### Checklist

- [ ] Schema is flat; types are standalone (User, Post, Comment—not nested)
- [ ] Resolver for each field is documented (which DB queries it makes)
- [ ] Dataloader is used for batch-loading related entities
- [ ] Slow resolvers are cached or optimized (profile first)
- [ ] Error handling is consistent (typed errors, clear messages)
- [ ] Mutations return the mutated object + errors in a consistent shape
- [ ] Subscriptions are tested (if used) with real clients
- [ ] Authorization middleware applies to sensitive fields
- [ ] Query complexity is limited (pagination, depth limit) to prevent DoS
- [ ] API documentation or schema comments explain when to use which query
