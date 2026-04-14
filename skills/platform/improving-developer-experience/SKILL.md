---
name: improving-developer-experience
description: Improves local setup, scripts, docs, task runners, and onboarding paths for faster developer flow. Use when repos are hard to bootstrap, inconsistent, or slow to work in.
when_to_use: developer experience, onboarding, dev setup
allowed-tools: Bash Read
---

## Local Dev Setup, Onboarding, and Tooling

Developer experience (DX) is force multiplier. Fast, clear setup and tools = faster onboarding and fewer bugs. The skill is automating setup, documenting workflows, and choosing tools that scale.

### When to Use

- New team member; setup takes >1 hour
- Complex local development (many services, databases)
- Frequent environment-specific bugs

### Decision Framework for Docker Compose, Make, or Devcontainers

1. **Docker Compose for local dev.** One docker-compose.yml starts all services (API, database, Redis, etc.). `docker compose up` = everything running.
2. **Makefile or npm scripts for commands.** `make dev`, `make test`, `make lint`. Consistent interface; no one has to remember flags.
3. **Devcontainers (VSCode) for isolation.** Development happens in container matching production. No "works on my machine" issues.
4. **README is a checklist.** Prerequisites (Node.js version, Docker), steps to run locally, common issues. New dev follows checklist; done in 30min.
5. **CI mirrors local tests.** Run same tests locally as in CI. No surprises on push.

### Anti-patterns to Avoid

- Manual setup steps. "Install X, run Y, set env var Z." Tedious and error-prone.
- Documentation is outdated. New team member follows README; steps fail. Frustration.
- Local dev differs from production. Service runs locally but fails in Docker. Debugging is painful.

### Checklist

- [ ] Docker Compose starts all services (`docker compose up`)
- [ ] README has setup checklist (prerequisites, steps, troubleshooting)
- [ ] `make dev` or `npm run dev` starts local environment
- [ ] `make test` runs same tests as CI
- [ ] No secrets in code; env vars are documented (with examples)
- [ ] Devcontainers (VSCode) or equivalent for reproducible dev environment
- [ ] New team member can run locally in <1 hour
- [ ] Local dev matches production (Node.js version, dependencies)
