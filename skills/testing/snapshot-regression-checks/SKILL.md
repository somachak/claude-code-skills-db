---
name: snapshot-regression-checks
description: Applies snapshot and golden-file testing carefully for stable outputs such as APIs, emails, rendered templates, and serialization. Use when outputs should remain consistent over time.
when_to_use: snapshot testing, golden file, approval testing
allowed-tools: "Read Bash(npm run test*) Bash(pytest*)"
---

## Snapshot Testing for UI and JSON

Snapshot tests capture output (rendered HTML, JSON, image) and alert on changes. Useful for regressions, but can become brittle. The skill is knowing when to use snapshots and when not to.

### When to Use

- Rendered component HTML (React, Vue)
- JSON responses (API output)
- Generated documents (PDFs, reports)
- Visual regressions (with pixel-diff tools)

### Decision Framework for Jest, Pytest, or Playwright

1. **Snapshots are regression detectors, not tests.** They don't assert correctness, only change. Use with unit/integration tests that verify behavior.
2. **Review snapshots in code review.** New snapshot? Diff is clear. Review change visually. Approve if intentional.
3. **Pixel-diff for visual regressions.** Use Percy, Chromatic, or similar for screenshot comparison. More robust than HTML snapshots for UI changes.
4. **Don't snapshot large objects.** Snapshot of entire user object (100 fields) = noisy diffs. Snapshot specific output.
5. **Intentional snapshot updates.** jest -u updates snapshots. Use when intentional change is made; commit diff in same PR.

### Anti-patterns to Avoid

- Snapshot as unit test. Snapshot changes, developer runs jest -u without thinking. Changed API contract, didn't notice.
- Huge snapshots. Diff is unreadable. Snapshot only relevant output.
- Snapshot with timestamps. Every run creates new snapshot due to datetime. Mock time or remove dynamic values.

### Checklist

- [ ] Snapshots are paired with unit/integration tests verifying behavior
- [ ] Snapshot diffs are reviewed in code review (intentional changes only)
- [ ] Snapshots don't contain timestamps or random data
- [ ] Large snapshots are broken into smaller, focused ones
- [ ] jest -u (snapshot update) is used intentionally, not blindly
- [ ] Pixel-diff tool used for visual regression (if applicable)
- [ ] Snapshot updates are documented in commit message
