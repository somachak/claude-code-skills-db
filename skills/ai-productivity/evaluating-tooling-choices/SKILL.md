---
name: evaluating-tooling-choices
description: Evaluates libraries, frameworks, and platform choices using adoption fit, migration cost, risk, and operational burden. Use when deciding between tools for frontend, backend, testing, or infrastructure work.
when_to_use: tool comparison, library choice, framework evaluation
---

## Decision Framework for Build Tools and Dependencies

Choosing the right tool (bundler, testing framework, ORM) affects productivity and maintenance burden for years. The skill is evaluating options systematically and documenting decisions.

### When to Use

- Choosing tech for new project
- Auditing existing tools (are they still the best choice?)
- Team is considering migration (webpack → Vite, Jest → Vitest)

### Decision Framework

1. **Evaluation criteria.** Performance, maintainability, community, learning curve, cost. Weight by importance to project.
2. **Trade-offs are explicit.** Webpack is slower than Vite, but has more loaders. Vitest is newer but faster. Document tradeoffs.
3. **Proof of concept.** Don't commit based on docs. Build prototype with candidate tool. Measure, compare.
4. **Decision record.** ADR (Architecture Decision Record) documents: what was the decision, why this tool, alternatives considered, tradeoffs. Helps future decisions.
5. **Sunsetting strategy.** If switching tools later, is it easy? If tool is proprietary, can you escape? Low switching cost preferred.

### Anti-patterns to Avoid

- Trendy choice. "Everyone uses X." X might not suit your project.
- One person decides. Tool is imposed on team. Resistance and resentment.
- No tradeoff analysis. Choose based on one metric (speed, not maintainability).

### Checklist

- [ ] Evaluation criteria are defined and weighted
- [ ] Candidates are evaluated against criteria
- [ ] Proof of concept is built (not just research)
- [ ] Decision is documented (ADR format)
- [ ] Team understands tradeoffs and rationale
- [ ] Migration cost is estimated (if switching later)
- [ ] Tool is evaluated annually (still best choice?)
