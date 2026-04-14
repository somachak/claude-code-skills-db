---
name: curating-team-conventions
description: Curates coding conventions, architectural defaults, and review standards into structured reference material that can later become skills. Use when teams repeat style, design, or workflow guidance.
when_to_use: team conventions, engineering standards, best practices
---

## Documentation, Linting, and Standardization

Team conventions (code style, PR size, file organization) scale culture. The skill is documenting conventions, automating enforcement, and evolving them.

### When to Use

- Onboarding new team member
- Code review becomes repetitive ("use const, not var")
- Merging teams or codebases with different standards

### Decision Framework

1. **Conventions are enforceable.** Use linters (ESLint, Ruff), formatters (Prettier, Black), TypeScript strict mode. Don't rely on code review alone.
2. **Conventions are documented.** CONTRIBUTING.md, ENGINEERING.md. New dev reads once; no questions.
3. **Conventions evolve.** Quarterly review. Does the convention still make sense? Vote, update, commit.
4. **Conventions are optional or required.** Style (const vs var)? Enforced by linter. Architecture? Manual review. Clarity on which is which.
5. **Conventions reflect tech stack.** React conventions differ from Next.js (Server Components). Document both.

### Anti-patterns to Avoid

- Undocumented conventions. Tribal knowledge. New dev doesn't know.
- Manual enforcement. Code review becomes nag-fest.
- Stale conventions. "We used to do that; ignore it."

### Checklist

- [ ] CONTRIBUTING.md or ENGINEERING.md documents conventions
- [ ] Linters enforce style (ESLint, Ruff, Prettier)
- [ ] Pre-commit hooks prevent violations
- [ ] PR template includes checklist (conventions checklist)
- [ ] Examples of good/bad code for conventions
- [ ] Conventions are reviewed and updated quarterly
- [ ] New dev can contribute without "unwritten rules"
- [ ] CI enforces linters (CI fails if violation)
