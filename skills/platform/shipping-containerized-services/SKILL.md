---
name: shipping-containerized-services
description: Packages services for containers with lean images, safe defaults, environment strategy, and deployment readiness checks. Use when containerizing APIs, workers, or internal tools.
when_to_use: dockerfile, container image, kubernetes deploy
allowed-tools: Bash Read
---

## Docker, Images, and Container Orchestration

Containers package code and dependencies. The skill is writing Dockerfiles that are secure, small, and fast to build.

### When to Use

- Deploying services to production (Kubernetes, ECS, Docker Swarm)
- Ensuring consistency across dev, staging, production
- Scaling services horizontally

### Decision Framework for Docker + Kubernetes or ECS

1. **Multi-stage builds reduce image size.** Build stage with build tools, runtime stage with only app + dependencies. Final image is 50% smaller.
2. **Base image matters.** Alpine (5MB) vs. Ubuntu (77MB). For Node.js, use node:22-alpine. For Python, python:3.11-slim.
3. **Layer caching aids iteration.** Layers that don't change are reused. Put COPY (changes frequently) after RUN (stable dependencies). Rebuild faster.
4. **Non-root user for security.** Don't run as root. Create app user; run process as app. Limits damage if container is compromised.
5. **Healthchecks enable orchestration.** Container reports healthy/unhealthy. Orchestrator (K8s) restarts unhealthy containers.

### Anti-patterns to Avoid

- Single-stage Dockerfile. Build tools in final image = bloat.
- Running as root. Compromise = full container access.
- Latest base image tag. Base image changes; build is non-reproducible. Pin version (node:22.3.0).

### Checklist

- [ ] Dockerfile uses multi-stage builds
- [ ] Base image is minimal (Alpine, Debian slim)
- [ ] Layer order optimizes cache (stable dependencies first)
- [ ] Non-root user is created; process runs as app user
- [ ] Healthcheck is defined
- [ ] Image is built and tested in CI before deploy
- [ ] Image size is <500MB (warn >1GB)
- [ ] Secrets (API keys, passwords) are not in image
