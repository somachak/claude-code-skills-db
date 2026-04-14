---
name: planning-multi-agent-work
description: Plans work decomposition, task boundaries, handoffs, and validation points for multi-agent development workflows. Use when parallelizing large refactors, research, or incident investigations.
when_to_use: subagents, parallel work, agent coordination
---

## Delegation and Async Coordination

Multi-agent systems (multiple Claude instances or team members working simultaneously) require clear specs, ownership, and sync points. The skill is decomposing tasks so agents can work in parallel.

### When to Use

- Large codebase changes requiring multiple agents/people
- Parallel work streams (API + web + database)
- Urgent tasks needing rapid execution

### Decision Framework for Claude Code Skills and Agents

1. **Spec is written first.** Agent reads spec; executes independently. No back-and-forth.
2. **Ownership is clear.** Agent A builds API endpoints; Agent B builds UI; Agent C integrates. No overlap or duplication.
3. **Interfaces are stable.** Agent B needs to know API contract (endpoint, request/response shape). Defined in spec, not emergent.
4. **Async by default.** Agents work on different files/systems; no waiting. Reduces coordination overhead.
5. **Sync points are explicit.** After API is built, Agent B starts UI. Spec defines these dependencies.

### Anti-patterns to Avoid

- Vague spec. "Build something." Agent wastes time guessing intent.
- Overlapping ownership. Two agents build same component; merge conflict.
- Synchronous work. Agent A builds API, Agent B waits. Serialize work unnecessarily.

### Checklist

- [ ] Spec is written and shared (clear intent, requirements)
- [ ] Ownership is assigned (Agent A: API, Agent B: UI)
- [ ] Interfaces are defined (API contract, data format)
- [ ] Dependencies are documented (A finishes before B starts)
- [ ] Agents work on different files/systems (no conflicts)
- [ ] Sync points are scheduled (integration check-in)
- [ ] Progress is tracked (status updates)
- [ ] Integration testing is planned (all components together)
