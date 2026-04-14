---
name: cataloging-codebase-patterns
description: Catalogs recurring codebase patterns, preferred implementations, and anti-patterns so future skills and prompts can reference real repository behavior. Use when onboarding to large codebases or consolidating conventions.
when_to_use: codebase patterns, preferred patterns, repository conventions
---

## Mining Code for Reusable Patterns

Large codebases have repeated patterns (API endpoint structure, form handling, error management). The skill is identifying and documenting patterns so new code follows them consistently.

### When to Use

- Codebase is >100K LOC with inconsistent patterns
- Onboarding is slow due to unclear patterns
- Code review repeats "we usually do this differently"

### Decision Framework

1. **Pattern is explicit, not implicit.** "Use react-query for API fetching" vs. "some use fetch, some axios, some react-query." Explicit wins.
2. **Pattern is documented with examples.** Not just "use error boundary for error handling." Show example, explain, show wrong way.
3. **Pattern is enforced by linting or convention.** Auto-enforcement is preferred (linting); manual review is fallback (conventions doc).
4. **Pattern is discoverable.** Developers know where to find it (ENGINEERING.md, Storybook, wiki).
5. **Pattern evolves.** "We used to do X; now we do Y" is documented. Reduces confusion.

### Anti-patterns to Avoid

- Implicit patterns. Experienced dev knows; new dev guesses.
- Inconsistent enforcement. Some code follows pattern; some doesn't. Confusing.
- Outdated patterns. "Old code uses middleware; new code uses hooks." Docs don't clarify which is preferred.

### Checklist

- [ ] Patterns are identified (API endpoints, form handling, error handling, etc.)
- [ ] Patterns are documented with examples (good and bad code)
- [ ] Examples are from actual codebase (not pseudocode)
- [ ] New code follows patterns (enforced in code review)
- [ ] Patterns are versioned (deprecated patterns are marked)
- [ ] Patterns are discoverable (linked from ENGINEERING.md)
- [ ] New dev learns patterns from docs, not osmosis
