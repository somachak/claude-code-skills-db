# Insecure Defaults Detection

**Category:** security-reliability · **Priority:** supporting · **Audience:** full-stack, backend

Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production. Distinguishes fail-open (CRITICAL: app runs with weak secret) from fail-secure (SAFE: app crashes if missing). Use when auditing security, reviewing config management, or analyzing environment variable handling.

## When Claude should reach for this

Trigger phrases: `insecure defaults`, `fail-open`, `hardcoded secrets`, `weak auth defaults`, `environment variable security`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
