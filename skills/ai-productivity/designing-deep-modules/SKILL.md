---
name: designing-deep-modules
description: Design modules with small interfaces and deep implementations using a precise shared vocabulary (module, interface, seam, adapter, depth). Use when designing or reviewing a module's interface, deciding where a seam goes, making code testable through its public surface, or collapsing pass-through layers in TypeScript or Python codebases.
when_to_use: module design, interface design, seams and adapters, testability review, collapsing pass-through layers
allowed-tools: Read Grep Glob
---

## Designing Deep Modules

A module is deep when a large amount of behaviour sits behind a small interface. Deep modules give callers leverage (more capability per unit of interface learned) and maintainers locality (changes, bugs, and knowledge concentrate in one place). Shallow modules -- big interface, thin pass-through implementation -- are the dominant failure mode in both TypeScript service code and Python backends: wrapper classes that re-export a client, "utils" barrels, three-method services where each method mirrors one ORM call.

### Vocabulary (use these terms exactly)

- **Module** -- anything with an interface and an implementation: a function, class, package, React hook, or FastAPI router + use-case slice. Scale-agnostic. Avoid: unit, component, service.
- **Interface** -- everything a caller must know to use the module correctly: type signature PLUS invariants, ordering constraints, error modes, required config, and performance characteristics. A TypeScript `interface` keyword is only the type-level sliver of this.
- **Seam** -- the place where behaviour can be swapped without editing call sites; the location of the interface. Deciding where the seam goes is a separate design decision from what goes behind it. Avoid: boundary (collides with DDD bounded context).
- **Adapter** -- a concrete thing satisfying an interface at a seam (Postgres repo, in-memory fake, Stripe gateway).

### The tests that settle arguments

1. **Deletion test.** Imagine deleting the module. If complexity simply vanishes, it was a pass-through -- inline it. If complexity reappears duplicated across N callers, it was earning its keep.
2. **The interface is the test surface.** Callers and tests should cross the same seam. If a test needs to reach past the interface (spying on internals, patching private methods), the module is the wrong shape -- widen the behaviour behind the interface or move the seam.
3. **One adapter means a hypothetical seam; two adapters means a real one.** Do not introduce an `IUserRepository` when only `PostgresUserRepository` will ever exist and no test uses a fake. Speculative seams are interface surface with no leverage.

### Designing for testability

- **Accept dependencies, don't construct them.** `processOrder(order, paymentGateway)` is testable; `new StripeGateway()` inside the function is not. In FastAPI, take dependencies through `Depends`/constructor injection; in TS, take them as parameters or a small context object -- not module-level singletons.
- **Return results, don't mutate arguments.** `calculateDiscount(cart): Discount` beats `applyDiscount(cart): void`. Pure-core / imperative-shell keeps the deep part of the module trivially testable.
- **Shrink the surface.** Fewer public methods means fewer tests needed and fewer invariants to document. Internal helpers can stay private and be exercised through the public interface.

### Deepening moves

- Collapse a cluster of shallow helpers that are always called together into one deep function with a domain name (`settleInvoice`, not `validateInvoice` + `computeTotals` + `markPaid` called in order by every caller).
- Pull caller-side boilerplate (retry, pagination, error mapping) inside the module so it is written once.
- A deep module may still have **internal seams** -- private parts swapped in its own tests -- without exposing them to callers.

### Anti-patterns

- **Pass-through layering:** controller calls service calls repository, each adding one line. Fails the deletion test twice.
- **Config leakage:** an interface that requires callers to know retry counts, table names, or header formats is shallow no matter how few methods it has -- those facts are interface too.
- **Interface = public methods:** if correct use requires calling `init()` before `run()`, that ordering constraint is part of the interface; either document it or redesign so misuse is impossible (make `run()` do init lazily, or return a ready object from a factory).
- **Depth as line-count ratio:** rewards padding the implementation. Measure depth as leverage: behaviour exercised per interface fact learned.

### Review checklist

- [ ] Can the number of public methods or parameters shrink?
- [ ] Does any caller knowledge (ordering, config, error handling) belong inside?
- [ ] Does every seam have -- or concretely anticipate -- a second adapter?
- [ ] Do tests cross only the public interface?
- [ ] Would deleting the module scatter real complexity into callers?
