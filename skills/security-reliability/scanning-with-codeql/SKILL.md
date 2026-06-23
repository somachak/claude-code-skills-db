---
name: scanning-with-codeql
description: Sets up CodeQL on TypeScript/JavaScript and Python repositories to find injection bugs, auth bypasses, and unsafe deserialization that pattern-based linters miss. Use when adding pre-merge security scanning to a Node, Next.js, FastAPI, or Django service, when triaging SARIF output from GitHub code scanning, or when writing custom queries for an internal API misuse class.
when_to_use: Hardening a Node/Next.js/FastAPI/Django service before launch, or triaging SARIF from GitHub code scanning.
---

## CodeQL Taint Analysis for Web Codebases

CodeQL is the right tool when a vulnerability class needs interprocedural data flow — Semgrep's intra-procedural taint stops at function boundaries. Reach for CodeQL when you're hunting injection, SSRF, prototype pollution, or insecure deserialization across module boundaries.

### When to Use

- A Node/Next.js or FastAPI/Django service is going through security review and you want a second opinion beyond ESLint/Bandit
- A bug class crossed module boundaries (e.g. tainted query param flowed three calls deep into `child_process.exec`) and you want to detect siblings
- You're triaging GitHub's default `security-extended` SARIF and need to tell true positives from noise
- You need a custom query for a project-specific sink — e.g. a wrapper around `subprocess.run` or a hand-rolled SQL builder

### When NOT to Use

- Style or single-line patterns — use Semgrep, ESLint, or ruff (10x faster, easier to author)
- Pure secret scanning — use gitleaks or trufflehog
- C/C++ memory safety (off-stack here; use sanitizers + fuzzing instead)

### Decision Framework

1. **Pick the right suite first.** `security-and-quality` is the default safety net; `security-extended` adds heuristics with more false positives; `security-experimental` for bleeding-edge queries. Don't enable `security-experimental` in blocking CI.
2. **Build the database from the same commit CI tests.** A stale database produces alerts that point at deleted code. Use `codeql database create db --language=javascript --source-root=. --command='npm ci && npm run build'` to capture the real build.
3. **JS and TS share a database.** Use `--language=javascript` even for TypeScript repos — the JS extractor handles `.ts` files. Python extracts cleanly with `--language=python` and needs no build step.
4. **Triage SARIF by sink, not by rule.** Group findings by the destination function (`exec`, `eval`, `os.system`, raw SQL). Each sink class shares a remediation pattern, so one fix can resolve many alerts.
5. **For custom queries, model first.** A data extension YAML that adds your internal `db.queryRaw(...)` as a SQL sink usually catches more bugs than a hand-rolled `.ql` query and is easier to maintain.

### Anti-patterns

- Enabling every suite and treating the result as ground truth — review the catalog and turn off rules that don't apply (e.g. `js/jquery-deprecated-symbols` in a React app).
- Running CodeQL on every push to `feat/*` branches — it's a 5-20 minute job. Run on `pull_request` to `main` and a nightly full scan instead.
- Treating an empty database extraction as success. Always assert the build step actually compiled — silently empty databases find zero issues.

### Worked Example — adding a custom Express sink

```yaml
# my-org-codeql/javascript/sinks.model.yml
extensions:
  - addsTo:
      pack: codeql/javascript-all
      extensible: sinkModel
    data:
      - ["my-org-sdk", "Member[runShell].Argument[0]", "command-injection"]
```

Then in workflow:

```yaml
- uses: github/codeql-action/init@v3
  with:
    languages: javascript
    config: |
      packs: [my-org/my-org-codeql]
```

### Validation Loop

- [ ] Database build command matches CI build (no skipped TS files)
- [ ] At least one known-good alert survives triage (proves the pipeline runs)
- [ ] SARIF is uploaded to GitHub or stored as an artifact for 90 days
- [ ] Custom queries have a `test/` directory with `.expected` files committed alongside
- [ ] Severity gating: `error`-level findings block the PR; `warning` is informational
