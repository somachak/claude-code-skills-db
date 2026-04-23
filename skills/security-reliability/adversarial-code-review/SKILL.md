---
name: adversarial-code-review
description: Forces genuine critical code review through three hostile personas — Saboteur, New Hire, and Security Auditor — each required to find at least one real issue. Eliminates rubber-stamp reviews and self-review blind spots. Use when reviewing your own code, when a second opinion is needed before merging, or when standard review missed issues in production. Different from generating-pr-reviews (which is collaborative feedback) and differential-review (which is security-change-focused).
---

# Adversarial Code Review

Three hostile reviewers. Each MUST find at least one real issue. No rubber-stamping.

## When to Use

- Reviewing your own code before merging (self-review blind spots are real)
- When a standard review passed but you want a harder look
- Pre-production review for sensitive features (auth, payments, data handling)
- When "looks good to me" reviews have let bugs through previously

## When NOT to Use

- Collaborative PR feedback where tone matters — use generating-pr-reviews skill
- Security-focused diff review of a specific change — use differential-review skill
- Quick style/formatting checks — use linters

## The Three Personas

### Persona 1: The Saboteur
Hunts for code that will break in production:
- **Validation gaps**: inputs that bypass validation, missing type coercions, off-by-one errors
- **State inconsistencies**: operations that leave data partially updated on failure
- **Concurrency issues**: race conditions, double-spending, lost updates under concurrent access
- **Resource leaks**: connections, file handles, goroutines, callbacks that never resolve
- **Error handling**: swallowed errors, silent failures, misleading error messages that mask the real failure

### Persona 2: The New Hire
Hunts for maintainability failures:
- **Unclear naming**: variables or functions whose names do not describe their actual behavior
- **Scattered logic**: the same concept implemented in three different places
- **Magic values**: undocumented numbers, strings, or constants with no explanation
- **Missing tests**: code paths that will silently break and no test will catch
- **Dead code**: unreachable branches, unused parameters, zombie feature flags

### Persona 3: The Security Auditor
Applies OWASP Top 10 patterns:
- **Injection**: user input flowing to SQL, shell commands, template engines, eval()
- **Auth bypass**: missing authorization checks, privilege escalation paths, insecure token handling
- **Data exposure**: PII/secrets in logs, debug endpoints in production, over-fetching in API responses
- **Access control**: horizontal privilege escalation (user A accessing user B's data)
- **Secrets**: hardcoded credentials, API keys in source, secrets in error messages

## Mandatory Finding Rule

**Each persona MUST find at least one issue.** If a persona finds nothing after genuine effort, the review was insufficiently thorough — try harder. "No issues found" is not an acceptable output.

## Severity Amplification

Issues flagged by two personas are promoted one severity level. Issues flagged by all three are promoted two levels and treated as BLOCK.

```
NOTE flagged by 2 personas  ->  WARNING
NOTE flagged by 3 personas  ->  CRITICAL
WARNING flagged by 2 personas  ->  CRITICAL
```

## Output Format

For each finding:

```
[PERSONA] SEVERITY: one-line summary
  Evidence: exact line/function reference
  Why it matters: concrete impact if not fixed
  Fix: specific, actionable recommendation
```

SEVERITY levels: NOTE / WARNING / CRITICAL

Verdict:
- **BLOCK** — one or more CRITICAL findings. Do not merge until resolved.
- **CONCERNS** — multiple WARNING findings. Should be addressed; merge only with sign-off.
- **CLEAN** — NOTE-level findings only. Document and merge at team's discretion.

## Anti-Patterns in This Review

- Cosmetic-only findings without a real impact statement
- Hedged language ("this might possibly be a concern") — be direct
- Generic findings ("improve error handling") without specifying which function and what the fix is
- Praising the code — this review is adversarial, not collaborative

## Example Finding

```
[SABOTEUR] CRITICAL: Cart checkout does not lock inventory before payment
  Evidence: checkout.ts:142 — reads inventory count, then processes payment, then decrements
  Why it matters: concurrent checkouts for the same low-stock item will both succeed,
                  resulting in negative inventory and oversold orders
  Fix: use a database transaction with SELECT FOR UPDATE on the inventory row
       before initiating payment, or use optimistic lock with retry on conflict
```
