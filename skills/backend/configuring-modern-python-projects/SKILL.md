---
name: configuring-modern-python-projects
description: Configures Python projects with modern tooling — uv for dependencies, ruff for lint and format, ty for type checking, PEP 735 dependency groups, PEP 723 inline script deps. Use when creating a new FastAPI or Django service, writing standalone scripts, or migrating a project from pip/Poetry/mypy/black.
---

## Modern Python Project Setup

Python's tooling has consolidated around a fast, coherent stack: uv (Astral) for dependencies and environments, ruff for lint/format, ty for type checking, and pyproject.toml as the single source of truth. This skill encodes the decisions that make a FastAPI or Django project feel clean instead of accreting config files.

### When to Use

- Bootstrapping a new FastAPI / Django service or internal Python library
- Writing a standalone script that needs third-party dependencies (PEP 723)
- Migrating a legacy project off pip + requirements.txt, Poetry, mypy, or black
- Adding a new dev dependency and wondering where it goes (groups vs extras)

### Decision Framework

1. **One package manager: uv.** Use `uv add <pkg>` and `uv remove <pkg>` to mutate `pyproject.toml`. Never hand-edit the `dependencies` array, and never run `uv pip install` — that bypasses the lockfile.
2. **Dev tooling in dependency-groups (PEP 735), not optional-dependencies.** `[dependency-groups]` is for contributor-only tools (pytest, ruff, ty). `[project.optional-dependencies]` is for end-user installable extras (e.g. `pip install myapp[postgres]`).
3. **Run commands via `uv run`.** `uv run pytest`, `uv run python manage.py migrate`, `uv run uvicorn app.main:app`. Don't source the venv manually — it's a stale pattern and breaks CI.
4. **Scripts use PEP 723.** A standalone `scripts/backfill.py` declares deps in a top-of-file comment block so `uv run scripts/backfill.py` resolves them on demand. Don't add script-only deps to the main project.
5. **Build backend: `uv_build`.** Simpler than hatchling and sufficient for apps and most libraries. Switch to hatchling only if you need plugin hooks or custom build steps.
6. **Types with ty, not mypy.** ty is faster, built by the ruff authors, and shares the same config surface. Set `[tool.ty.environment] python-version = "3.12"` — note the nested table, not the flat `[tool.ty]`.

### Anti-patterns

| Avoid | Use Instead |
|-------|-------------|
| `uv pip install requests` | `uv add requests` |
| `source .venv/bin/activate && pytest` | `uv run pytest` |
| `requirements.txt` + `requirements-dev.txt` | `pyproject.toml` + `[dependency-groups]` |
| `[tool.black]` + `[tool.isort]` + `[tool.flake8]` | `[tool.ruff]` (one tool, one config) |
| Hand-editing `pyproject.toml` to add deps | `uv add` / `uv remove` |
| `mypy` for new projects | `ty` |
| Poetry for new projects | uv |
| Mixing sync `requests` into a FastAPI handler | `httpx.AsyncClient` |

### Worked Example — FastAPI service

```bash
uv init --package svc-users && cd svc-users
uv add fastapi 'uvicorn[standard]' sqlalchemy asyncpg pydantic-settings
uv add --group dev pytest pytest-asyncio ruff ty httpx
uv run ruff check --fix
uv run ty check
uv run pytest
```

Resulting `pyproject.toml` skeleton:

```toml
[project]
name = "svc-users"
requires-python = ">=3.12"
dependencies = ["fastapi", "uvicorn[standard]", "sqlalchemy", "asyncpg", "pydantic-settings"]

[dependency-groups]
dev = ["pytest", "pytest-asyncio", "ruff", "ty", "httpx"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]

[tool.ty.environment]
python-version = "3.12"
```

### Checklist

- [ ] Project uses `uv` and has a committed `uv.lock`
- [ ] Dev tools live in `[dependency-groups]`, not `[project.optional-dependencies]`
- [ ] `ruff check` and `ruff format` both pass; no black/isort/flake8 configs left behind
- [ ] `ty check` passes; no mypy config remaining
- [ ] CI runs `uv sync --frozen` and `uv run` commands — no manual venv activation
- [ ] Standalone scripts use PEP 723 inline metadata, not the project's deps
