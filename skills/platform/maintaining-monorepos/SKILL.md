---
name: maintaining-monorepos
description: Maintains monorepos through workspace boundaries, task graph design, ownership rules, and incremental validation. Use when scaling packages, apps, services, and shared libraries together.
when_to_use: monorepo, workspace graph, nx
allowed-tools: Bash Read
---

## Workspace Layout, Dependencies, and Tooling

Monorepos (single repo, multiple projects) reduce friction but add complexity. The skill is structuring workspaces, managing dependencies, and enabling independent deployment.

### When to Use

- Multiple related services (API, web app, CLI) in one repo
- Shared libraries and utilities
- Coordinating changes across services

### Decision Framework for Lerna, Nx, Turborepo, or pnpm Workspaces

1. **Clear folder structure.** /packages/api, /packages/web, /packages/shared. Each package has own package.json.
2. **Shared libraries via symlink.** Monorepo tool symlinks shared packages into node_modules. Code changes instantly reflected.
3. **Build graph for incremental builds.** Only rebuild packages that changed. If shared library changed, rebuild dependents.
4. **Publishing from monorepo.** Each package has version, changelog, publish trigger. Coordinated but independent releases.
5. **Dependency management.** Monorepo tool ensures versions are consistent (shared library same version everywhere).

### Anti-patterns to Avoid

- Copy-paste code across packages. Monorepo exists to share. Shared library should be explicit.
- Tight coupling between packages. One change breaks unrelated package. Defeats scaling.
- No build isolation. Webpack for web, Node for API in same repo. Build tool conflicts.

### Checklist

- [ ] Folder structure is clear (/packages/api, /packages/web, /packages/shared)
- [ ] Each package has own package.json and tsconfig.json
- [ ] Monorepo tool (Lerna, Nx, Turborepo) manages dependencies
- [ ] Build graph is incremental (only changed packages rebuilt)
- [ ] Shared library is symlinked and changes are instant
- [ ] Each package can be deployed independently
- [ ] Dependency versions are consistent across packages
- [ ] CI runs tests only for changed packages (--since flag)
