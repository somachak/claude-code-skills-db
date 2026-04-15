---
name: designing-property-based-tests
description: Identifies code patterns where property-based testing produces stronger coverage than example-based tests — serialization pairs, parsers, normalizers, validators, pure functions. Use when writing tests for TypeScript, Node, or Python code that encodes, parses, normalizes, or validates user input.
---

## Property-Based Testing Playbook

Example-based tests check specific inputs. Property-based tests (PBT) generate thousands of inputs and check invariants — roundtrips, idempotence, ordering, structural properties. PBT shines on the exact code paths where example tests usually miss edge cases: encoders, parsers, normalizers.

Tooling: `fast-check` for TypeScript/Node, `hypothesis` for Python.

### When to Invoke

Reach for PBT when you see:

| Pattern | Property | Priority |
|---------|----------|----------|
| `encode` / `decode` pair | Roundtrip: `decode(encode(x)) === x` | HIGH |
| Parser (URL, config, protocol) | Structural invariants on output | HIGH |
| Pure function over a domain | Algebraic laws (associativity, identity) | HIGH |
| Normalizer (`sanitize`, `canonicalize`) | Idempotence: `norm(norm(x)) === norm(x)` | MEDIUM |
| Validator | `valid(normalize(x))` for any x in domain | MEDIUM |
| Comparator / sort | Transitivity, stability | MEDIUM |
| Data structure (add/remove/get) | Model-based oracle | MEDIUM |

### When NOT to Use

- Simple CRUD with no transformation logic — a few example tests are clearer
- Code with unmockable side effects (network, disk, database writes)
- Throwaway scripts or one-off migrations
- Cases where specific regression examples carry the intent better than a property

### Decision Framework

1. **Find the invariant first, then write the test.** "What must always be true about this function's output?" is the correct starting question. If you can't name a property in one sentence, example tests are probably a better fit.
2. **Constrain generators to the real input domain.** Unbounded `fc.string()` will trip over Unicode surrogates your code will never actually see. Use `fc.string({unit: "grapheme-ascii"})` or a custom arbitrary matching your validator.
3. **Shrink-friendly shapes.** Prefer `fc.record({...})` over raw tuples so failing counterexamples are readable. Give each arbitrary a `.filter()` only as a last resort — filter rejection kills throughput.
4. **Model-based tests for stateful code.** For a cache or queue, define a reference implementation in plain code and check that sequences of operations produce matching observations. `fc.commands` and Hypothesis `RuleBasedStateMachine` do this well.
5. **Pin the seed on failure.** When CI surfaces a counterexample, copy the seed into a regular unit test alongside the property. That way the bug stays pinned even if the generator evolves.

### Worked Example — fast-check (TypeScript)

```ts
import fc from "fast-check";
import { encode, decode } from "./codec";

test("codec roundtrip", () => {
  fc.assert(fc.property(fc.record({ id: fc.uuid(), name: fc.string() }), (x) => {
    expect(decode(encode(x))).toEqual(x);
  }));
});

test("encode is deterministic", () => {
  fc.assert(fc.property(fc.record({ id: fc.uuid(), name: fc.string() }), (x) => {
    expect(encode(x)).toEqual(encode(x));
  }));
});
```

### Worked Example — Hypothesis (Python / FastAPI)

```python
from hypothesis import given, strategies as st
from app.normalize import slugify

@given(st.text())
def test_slugify_is_idempotent(s):
    assert slugify(slugify(s)) == slugify(s)

@given(st.text())
def test_slugify_output_is_url_safe(s):
    import re
    assert re.fullmatch(r"[a-z0-9-]*", slugify(s))
```

### Anti-patterns

- Writing a property that just restates the implementation (`assert sort(xs) == sorted(xs)`) — tautological.
- Ignoring shrinking output; debugging `["\u{D800}"]` when you meant ASCII.
- Mixing PBT with network calls — non-deterministic, flaky, wastes CI minutes.
- Using PBT to replace integration tests instead of complementing them.

### Checklist

- [ ] Named the invariant in plain English before coding
- [ ] Generators match the real input domain (no unintentional Unicode / giant numbers)
- [ ] At least one property per: roundtrip, idempotence, or output invariant
- [ ] Stateful code has a model-based test, not just per-operation properties
- [ ] Counterexamples from CI get pinned as regular unit tests
