---
name: authoring-semgrep-rules
description: Writes, tests, and ships custom Semgrep rules that catch project-specific security bugs and anti-patterns in TypeScript, Node, Python, FastAPI, and Django codebases. Use when adding lint coverage for a vulnerability class, codifying a postmortem, or building taint rules for user-input-to-sink flows.
---

## Custom Semgrep Rule Authoring

Semgrep is the fastest path from "we just shipped a bug class, don't do it again" to "CI blocks the PR that reintroduces it." This skill covers writing production-quality rules with proper tests — not just patterns that look plausible.

### When to Use

- A postmortem identified a bug class worth preventing at the lint layer
- You want to flag an internal API misuse (e.g. raw SQL in Django, unsafe `jsonify` in FastAPI)
- You need taint tracking from user input (request params, headers) to a dangerous sink (shell, eval, SQL, file path)
- You're enforcing a team convention that AST matching can express (no `any`, no `console.log` in production paths)

### When NOT to Use

- Running existing rulesets (that's `semgrep ci` — no custom authoring needed)
- Style-only issues already covered by ESLint, ruff, or Prettier — let those tools handle it
- Patterns that require whole-program data flow beyond Semgrep's intra-procedural taint (use CodeQL)

### Decision Framework

1. **Start with a failing test, not a pattern.** Create `rule.yaml` alongside `rule.ts` (or `.py`) containing both vulnerable and safe examples. Mark the vulnerable lines with `// ruleid: <rule-id>` and safe lines with `// ok: <rule-id>`. Write the pattern until `semgrep --test --config rule.yaml rule.ts` passes.
2. **Pattern first, optimize later.** Get `pattern:` matching the vulnerability, then tighten with `pattern-not:`, `pattern-either:`, `pattern-inside:`. Premature metavariable regex usually causes false negatives.
3. **Use taint mode for dataflow.** If the rule is "user input reaches SQL," taint mode (`mode: taint` with `pattern-sources` / `pattern-sinks`) is far more precise than chained pattern matching.
4. **Write the message like a reviewer.** Short description + why it's bad + suggested fix. Developers will see this hundreds of times — make it teach, not nag.
5. **Pick severity honestly.** `ERROR` blocks CI; reserve it for actual security bugs. `WARNING` for design issues. `INFO` for style nudges.

### Worked Example — FastAPI unsafe redirect

```yaml
rules:
  - id: fastapi-open-redirect
    message: >
      Redirecting to a value taken directly from request parameters allows
      attacker-controlled URLs. Validate that the target is an allow-listed
      path or absolute URL under your own domain.
    severity: ERROR
    languages: [python]
    mode: taint
    pattern-sources:
      - pattern-either:
          - pattern: $REQ.query_params.get(...)
          - pattern: $REQ.query_params[...]
    pattern-sinks:
      - patterns:
          - pattern: RedirectResponse($URL, ...)
          - pattern: fastapi.responses.RedirectResponse($URL, ...)
    pattern-sanitizers:
      - pattern: validate_redirect_target(...)
```

Tests in `fastapi-open-redirect.py`:

```python
from fastapi import Request
from fastapi.responses import RedirectResponse

def bad(req: Request):
    target = req.query_params.get("next")
    # ruleid: fastapi-open-redirect
    return RedirectResponse(target)

def good(req: Request):
    target = validate_redirect_target(req.query_params.get("next"))
    # ok: fastapi-open-redirect
    return RedirectResponse(target)
```

### Rationalizations to Reject

- **"The pattern looks complete."** Run `semgrep --test` anyway. Untested rules have hidden FPs/FNs.
- **"It catches the vulnerable case."** Matching vulnerabilities is half the job. Verify safe cases don't match — false positives are how rules get disabled.
- **"Taint is overkill here."** If user input flows to a sink, taint mode gives you sanitizer support for free. You'll want it.
- **"I'll optimize first."** Correctness first. Optimize metavariable regexes after all tests pass.
- **"One test example is enough."** Add at least: the exact bug, a near-miss that must not match, and the sanitized/safe version.

### Checklist

- [ ] Rule has paired test file with `ruleid:` and `ok:` markers
- [ ] `semgrep --test --config rule.yaml rule.<ext>` passes with zero false positives/negatives in the test corpus
- [ ] Message explains the bug, the risk, and the fix — not just the pattern
- [ ] Severity chosen deliberately (ERROR blocks CI)
- [ ] For taint rules: sources, sinks, and sanitizers all listed
- [ ] Rule id prefixed with team/project namespace so it doesn't collide with registry rules
