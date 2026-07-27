---
name: auditing-unit-consistency
description: "Apply dimensional analysis to application code: assign units (cents, ms, percent, tokens) to every quantity, propagate them through arithmetic, and flag dimensionally impossible operations. Use when auditing pricing, billing, quota, scheduling, or analytics code for unit-mismatch bugs, mixed scales, precision loss, or money-in-floats problems that type checkers cannot catch."
when_to_use: auditing arithmetic-heavy code for unit mismatches, mixed scales, percent vs ratio confusion, or float-money bugs
allowed-tools: Read Grep Glob Bash
---

## Auditing Unit Consistency

Numeric code that mixes units, scales, or precisions is a reliable source of severe, hard-to-spot bugs: cents added to dollars, milliseconds compared to seconds, percentages multiplied where basis points were meant, token amounts with 6 decimals combined with 18-decimal amounts. Type checkers don't catch these -- `number + number` and `int + int` are always well-typed. This skill applies dimensional analysis (the physics technique) to application code: assign every quantity a unit, propagate units through arithmetic, and flag operations that are dimensionally impossible.

### Step 1: Build the unit vocabulary

Scan the code that does arithmetic (pricing, billing, quotas, scheduling, analytics, conversions) and write down the repo's actual units before judging anything:

- **Base units:** `cents`, `usd`, `ms`, `s`, `bytes`, `tokens`, `rows`, `percent` (0-100), `ratio` (0-1), `bps`.
- **Derived units:** `usd/token`, `req/s`, `bytes/row`.
- **Scale prefixes:** fixed-point decimals (`e2` for cents, `e6`/`e18` for token amounts), `milli`, `kilo`.

Record the vocabulary in a short reference (comment block or `UNITS.md`) so later passes and other reviewers reuse the same names.

### Step 2: Annotate anchors

Anchor points are places where a unit is known for certain: API boundaries ("Stripe amounts are integer cents"), DB columns (`duration_ms INTEGER`), config ("timeout in seconds"), library contracts (`Date.now()` is ms, `time.time()` is float seconds). Annotate them with unit comments:

```ts
const amountCents = invoice.total;      // unit: cents (Stripe)
const timeoutS = config.timeout;        // unit: s
const elapsed = Date.now() - startedAt; // unit: ms
```

Prefer encoding units in names (`amountCents`, `timeoutMs`) and, where the codebase supports it, in types (branded types in TS: `type Cents = number & { __brand: "cents" }`; `NewType` in Python).

### Step 3: Propagate and check

Push units through each expression using the algebra: addition/subtraction/comparison require identical units; multiplication/division combine them; assignment to an annotated target must match.

- `cents + cents = cents` -- fine. `cents + usd` -- bug or missing conversion.
- `usd/token * tokens = usd` -- fine. `usd/token * usd` -- dimensionally impossible; flag it.
- `if (elapsedMs > timeoutS)` -- comparison across scales; near-certain bug.
- `total * discountPercent` where `discountPercent` is 0-100 and result is used as a ratio -- off-by-100.

### Red flags to hunt directly

- `* 100`, `/ 100`, `* 1000`, `/ 1000` scattered near each other -- often one conversion too many or too few.
- Floats holding money (`0.1 + 0.2 !== 0.3`); money should be integer cents/base units or a decimal type.
- Two variables with the same name and different units in different files (`timeout` as ms in one module, s in another).
- Division before multiplication on integers -- silent precision loss (`a / b * c` vs `a * c / b`).
- JSON/DB round-trips that change scale (storing seconds, reading as ms).

### Validate before reporting

For each suspected mismatch, reject rationalizations: "it cancels out later" and "the values are small" are not fixes. Confirm by tracing one concrete value end-to-end (e.g. a $12.34 invoice: 1234 cents in, what comes out?). Report each confirmed finding with the expression, the units of each operand, the expected unit, and the concrete wrong result.

### Checklist

- [ ] Unit vocabulary written down and reused
- [ ] All external boundaries (APIs, DB, config, stdlib time) annotated
- [ ] Every +, -, comparison checked for identical units
- [ ] Every * and / produces a unit somebody actually wants
- [ ] Money is integers or decimals, never binary floats
- [ ] One worked numeric example per confirmed finding
