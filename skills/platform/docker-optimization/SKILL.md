---
name: docker-optimization
description: Optimizes Dockerfiles and docker-compose configurations for image size, build speed, layer caching, and security hardening. Use when Dockerfiles are slow to build, images are bloated, containers run as root, or docker-compose files need production hardening. Covers multi-stage builds, .dockerignore strategy, secret handling, non-root users, healthchecks, and base-image selection for Node.js, Python, and compiled binaries. Different from shipping-containerized-services which handles deployment readiness.
---

# Docker Optimization

Optimize Dockerfiles and docker-compose for production: smaller images, faster builds, better security.

## When to Use

- Dockerfile builds are slow (>60s on cached layers)
- Images are larger than 500MB for interpreted languages or 100MB for compiled
- Containers run as root (security risk)
- docker-compose files need production hardening
- Multi-stage builds are absent or poorly structured
- Secrets are embedded in image layers

## When NOT to Use

- Kubernetes deployment manifests — use managing-infrastructure-as-code skill
- Service deployment strategy (blue/green, rolling) — out of scope here
- Registry auth and image signing — handled by hardening-ci-pipelines skill

## Anti-Patterns

- **`:latest` tags** — unpredictable, breaks reproducibility. Always pin: `node:20.11-alpine3.19`
- **`RUN apt-get install` without cleanup** — leaves cache in the layer, inflates image. Always end with `&& rm -rf /var/lib/apt/lists/*`
- **Copying source before dependencies** — invalidates dependency cache on every code change. Copy `package.json` first, install deps, THEN copy source.
- **Running as root** — any RCE exploit gets full container privileges. Always add `USER nonroot` before CMD.
- **Secrets in ENV instructions** — stored in image history, visible via `docker history`. Use BuildKit secrets or runtime env injection.
- **No .dockerignore** — copies node_modules, .git, test fixtures into build context. Always create a .dockerignore.

## Base Image Decision Tree

Need a compiled binary only? Use distroless/static or scratch.
Interpreted language (Python/Node/Ruby)? Use `{language}:{version}-alpine` (smallest) or `{language}:{version}-slim` if alpine has compatibility issues.
Need specific OS packages? Use `debian:bookworm-slim`.
Avoid full ubuntu/debian unless truly needed — no benefit over slim variants.

## Multi-Stage Pattern (Node.js Example)

```dockerfile
# Stage 1: build dependencies only
FROM node:20.11-alpine3.19 AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: build application
FROM node:20.11-alpine3.19 AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: minimal production image
FROM node:20.11-alpine3.19 AS runner
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

## Layer Caching Rules

Order Dockerfile instructions by change frequency (least to most frequent):
1. Base image and system deps (rarely changes)
2. Package manifests (package.json, requirements.txt, Cargo.toml)
3. Dependency installation (npm ci, pip install, cargo build)
4. Application source code (changes every commit)

## Security Checklist

- [ ] No root user in final stage (USER nonroot or equivalent)
- [ ] No secrets in ENV or ARG instructions (use BuildKit --secret)
- [ ] Pinned base image tag (not :latest)
- [ ] HEALTHCHECK present
- [ ] .dockerignore excludes: node_modules/, .git/, .env*, *.test.*, coverage/
- [ ] Read-only filesystem where possible (--read-only at runtime)
- [ ] No unnecessary capabilities (drop ALL, add back only what is needed)

## docker-compose Production Hardening

Key fields to add to every production service:
- `restart: unless-stopped`
- `read_only: true` with `tmpfs: [/tmp]` for scratch space
- `security_opt: [no-new-privileges:true]`
- `cap_drop: [ALL]` — add back only what is required
- `healthcheck` with a real test command

## Python-Specific Pattern (uv)

```dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY src/ ./src/
RUN adduser --system appuser && chown -R appuser /app
USER appuser
```
