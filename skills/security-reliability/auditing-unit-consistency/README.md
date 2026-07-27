# Auditing Unit Consistency

**Category:** security-reliability · **Priority:** supporting · **Audience:** back-end, data, security

Apply dimensional analysis to application code: assign units (cents, ms, percent, tokens) to every quantity, propagate them through arithmetic, and flag dimensionally impossible operations. Use when auditing pricing, billing, quota, scheduling, or analytics code for unit-mismatch bugs, mixed scales, precision loss, or money-in-floats problems that type checkers cannot catch.

## When Claude should reach for this

Trigger phrases: `unit mismatch`, `dimensional analysis`, `cents vs dollars`, `milliseconds vs seconds`, `audit numeric code`, `precision loss`, `money in floats`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
