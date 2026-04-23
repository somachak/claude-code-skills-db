---
name: audit-context-building
description: "Builds ultra-granular architectural context through systematic line-by-line code analysis before vulnerability hunting. Use before security audits, threat modeling sessions, or any deep code review where superficial understanding risks missing subtle bugs. Five-phase: orientation, micro-analysis per function, global system reconstruction, stability rules, integration. Do NOT use for generating vulnerability findings — this is the pre-audit context phase only."
---

# Audit Context Builder

Build ultra-granular architectural context before security audits. This skill drives the mandatory context phase — it does NOT produce vulnerability findings. Findings come after.

## When to Use

- Starting a security audit of an unfamiliar codebase
- Before any deep vulnerability hunt where missing context would cause false negatives
- Architecture review requiring full state-machine understanding
- Any review where "I get the gist" thinking is dangerous

## When NOT to Use

- Do NOT use for generating vulnerability findings (use threat-modeling or differential-review skills)
- Do NOT use for fix recommendations
- Do NOT use for quick code scans — this is deliberate, exhaustive work

## Anti-Patterns to Reject

- **"I get the gist"** — Never skip micro-analysis because a function "looks obvious." Assumptions embed bugs.
- **"External calls are black boxes"** — For external contracts/libraries with available source, apply the same micro-analysis. For true black boxes, assume adversarial behavior.
- **"Global understanding can wait"** — Phase 3 (global system reconstruction) unlocks cross-function vulnerabilities that per-function analysis misses entirely.
- **"Invariants are obvious"** — Document minimum three invariants per function explicitly. Surprises live in the gaps between assumed invariants.

## Five-Phase Workflow

### Phase 1 — Initial Orientation
Map the system before reading any function body:
- Identify all modules, packages, entrypoints
- List all external actors and their trust levels
- Catalog all storage variables and their types
- Draw the high-level call graph (even rough is fine)

### Phase 2 — Ultra-Granular Function Analysis
For EVERY function in scope, document:
- **Purpose**: single sentence stating what this function does
- **Inputs**: each parameter with its preconditions and trusted/untrusted classification
- **Outputs**: return values and all state side-effects
- **Block-by-block reasoning**: walk each block using First Principles — state what changes and why
- **Invariants**: minimum 3 invariants that must hold on entry and exit
- **Assumptions**: minimum 5 assumptions this function makes about callers/callees
- **Cross-function deps**: which functions this must call before/after, and in which order

### Phase 3 — Global System Understanding
After all functions are analyzed, reconstruct:
- Full state machine: every state variable and all its possible transitions
- Workflow sequences: the ordered multi-step flows that produce each observable outcome
- Trust boundaries: where untrusted data enters and where it can propagate to

### Phase 4 — Stability Rules
Apply throughout analysis to prevent hallucination:
- Never infer behavior from function names alone — read the body
- Explicitly mark uncertainty: "UNCERTAIN: this assumes X" rather than stating X as fact
- If two functions conflict in their documented behavior, flag the discrepancy rather than resolving it
- Do not skip files — maintain a checklist and verify every in-scope file completes all phases

### Phase 5 — Integration
Connect findings across function boundaries:
- Identify sequences where Phase 2 assumptions conflict between callers and callees
- Flag any invariant that a caller violates when invoking a callee
- Produce a final cross-function dependency graph with trust annotations

## Checklist Before Handing Off to Audit Phase

- [ ] Every in-scope function has Purpose, Inputs, Outputs, Block reasoning, Invariants, Assumptions
- [ ] All external calls classified: source-available (analyzed) or black-box (adversarial assumption)
- [ ] Global state machine documented
- [ ] All entry points and their trust levels listed
- [ ] No "I get the gist" shortcuts taken — all uncertainty explicitly flagged
- [ ] Cross-function dependency graph produced

## Decision: When to Use Subagents

For codebases >5,000 lines, delegate each module to a subagent for Phase 2. The main context must not substitute its own reasoning for a module a subagent was assigned. Collect all subagent outputs before starting Phase 3.
