---
name: spec-driven-development
description: Enforces writing a complete specification before any implementation begins. Use when starting a new feature, API, or subsystem — especially when working with AI coding agents that over-implement. Produces a nine-section spec with RFC 2119 requirements, acceptance criteria, and test stubs before a single line of code is written. Catches scope creep and ambiguity early. Different from designing-workflow-skills (which designs skills) and designing-rest-apis (which designs API contracts).
---

# Spec-Driven Development

**Core rule: no implementation begins without an approved specification.** No exceptions.

## When to Use

- Starting any new feature, API endpoint, subsystem, or service
- When AI coding agents tend to over-implement or drift from requirements
- When you need a binding contract between product intent and engineering output
- When acceptance criteria need to be defined before code is written
- Greenfield services, breaking API changes, complex business logic

## When NOT to Use

- Trivial bug fixes with a single, obvious fix
- Pure refactors with no behavior change (write tests instead)
- Exploratory spikes where the goal IS ambiguity resolution

## The Nine-Section Spec Template

Every spec must contain all nine sections — no partial specs are accepted:

1. **Title and Metadata** — feature name, author, date, status (Draft / Approved / Superseded)
2. **Context** — why this feature exists; what problem it solves and for whom
3. **Functional Requirements** — MUST/SHOULD/MAY statements per RFC 2119; each requirement gets an ID (FR-01, FR-02...)
4. **Non-Functional Requirements** — latency, throughput, error budget, security constraints
5. **Acceptance Criteria** — testable binary conditions (pass/fail); maps 1:1 to test stubs in Phase 4
6. **Edge Cases** — explicit enumeration of boundary conditions, error states, race conditions
7. **API Contracts** — request/response schemas or function signatures with types
8. **Data Models** — database schema changes, event payloads, state machine diagrams
9. **Explicit Exclusions** — list what is NOT in scope; prevents gold-plating

## Six-Phase Workflow

**Phase 1 — Gather Requirements**
Ask: Who is the actor? What is the trigger? What is the expected outcome? What are the constraints?

**Phase 2 — Write Spec**
Complete all nine sections. Use RFC 2119 keywords throughout. Every acceptance criterion must be binary (testable true/false). Every API field must have a type and nullability.

**Phase 3 — Validate Spec**
Run these checks before marking Approved:
- [ ] Every functional requirement has at least one acceptance criterion
- [ ] Every acceptance criterion is binary (testable)
- [ ] Edge cases cover: empty inputs, max-size inputs, concurrent access, partial failure
- [ ] No vague criteria ("should be fast" is rejected; "p95 < 200ms under 100 RPS" is accepted)
- [ ] Exclusions section prevents over-scoping

**Phase 4 — Generate Tests**
Extract each acceptance criterion into a test stub. The stub must: name the criterion, declare its inputs, state the expected output. No implementation logic yet.

**Phase 5 — Implement**
Write code that makes the test stubs pass. Each commit should reference the spec requirement ID it implements (e.g., `implements FR-03`).

**Phase 6 — Self-Review**
Before closing: verify every acceptance criterion passes, every functional requirement is implemented, no behavior was added beyond the spec.

## Anti-Patterns

- **Vague criteria**: "The API should handle errors gracefully" — rejected. Write the specific error code and response body.
- **Missing exclusions**: not stating what is out of scope invites scope creep.
- **Gold-plating**: implementing beyond the spec is a spec violation, even if "nice to have."
- **Spec-as-afterthought**: writing spec after code defeats the purpose — the spec IS the source of truth.
- **Ambiguity threshold**: if >30% of requirements are ambiguous after one clarification round, stop and escalate. Do not guess.

## Escalation Triggers

Pause implementation and escalate to a human when:
- Scope creep is detected (work required exceeds spec)
- A requirement conflicts with another requirement
- The implementation would require a breaking API change not anticipated in the spec
- A security implication emerges that the spec did not address
- Cross-team dependencies appear that were not declared

## Bounded Autonomy

For non-breaking, fully-specified work: proceed autonomously. For anything that crosses an escalation trigger: stop, document the blocker, and await resolution before continuing.
