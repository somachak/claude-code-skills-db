---
name: evaluating-skill-performance
description: "Measures whether a Claude skill actually helps: paired with-skill vs baseline runs spawned together, objective assertions for verifiable outputs and human judgment for subjective ones, transcript review for wasted work, and a 20-query trigger eval set (near-miss negatives included) for optimizing the description field that controls invocation. Use when a skill has been written but never measured, when iterating on a skill that fires inconsistently or not at all, or when deciding whether a change to a skill body was actually an improvement."
when_to_use: Use after writing or editing a Claude skill, when a skill triggers on the wrong prompts or fails to trigger, or when a skill change needs to be validated against a baseline.
---

## Evaluating Skill Performance

A skill that has never been measured is a hypothesis. This is the loop for turning one into a known quantity: run it against a baseline, grade the difference, and tune the description until it fires when it should and stays quiet when it shouldn't.

Two separate things get measured, and conflating them wastes iterations:

- **Body quality** — given that the skill fired, is the output better than without it?
- **Trigger accuracy** — does the skill fire on the right prompts at all?

### Part 1 — Body quality: always run a baseline

The single most common mistake is evaluating a skill without a control. The model is capable; much of what looks like skill-driven improvement is just the model being good. Without the baseline you cannot tell.

**Spawn both arms in the same turn**, not sequentially:

- *With-skill* arm: the task prompt plus the skill path.
- *Baseline* arm: identical prompt, **no skill** (for a new skill) or **a snapshot of the previous version** (for an improvement). Snapshot before editing — `cp -r <skill> <workspace>/skill-snapshot/` — or you lose the comparison.

Store results as `<skill>-workspace/iteration-N/<eval-name>/{with_skill,baseline}/`. Name evals for what they test, not `eval-0`.

While runs are in flight, draft assertions. Assertions must be objectively checkable — file exists, column present, no hardcoded hex values, all links resolve. **Do not force assertions onto subjective skills.** Writing tone and visual design are graded qualitatively by the user; a fake rubric on a subjective skill produces confident nonsense.

**Read the transcripts, not just the outputs.** The output tells you whether it worked. The transcript tells you *why*, and it's where you see the skill sending the model down a 4-step detour that a single sentence could have prevented.

### Part 2 — Improving without overfitting

You iterate on 3–5 examples; the skill will run thousands of times. Everything you change is at risk of fitting the examples rather than the task.

| Symptom | Bad fix | Better fix |
|---|---|---|
| Model misses a step | Add "ALWAYS do X" in caps | Explain *why* X matters, so it generalizes |
| Output has the wrong shape | Add a rigid template | Show one worked example of the right shape |
| Model wastes turns | Add more instructions | **Delete** the instruction causing the detour |
| One eval still fails | Add a clause naming that case | Reframe with a different metaphor and re-run all evals |

Yellow flag: if you're writing ALWAYS or NEVER in caps, you're compensating for an unexplained rule. Explain the reason instead — modern models follow reasoning further than they follow commands.

Green flag: the skill got **shorter** and scores stayed flat or improved. Lean prompts generalize; every sentence that isn't pulling its weight is competing for attention with one that is.

### Part 3 — Description optimization

The `description` field is the entire mechanism by which the skill gets selected. Tune it with a real eval set, not by intuition.

Build **20 queries: 8–10 should-trigger, 8–10 should-not-trigger.** Quality of these queries determines everything:

- Write what a user would actually type — file paths, real column names, company names, a little backstory, lowercase, typos, casual phrasing.
- Bad positive: `"Format this data"`. Good positive: `"boss sent me a xlsx in my downloads called 'Q4 sales final FINAL v2.xlsx', need a profit margin % column, revenue's in C and cost in D i think"`.
- **Negatives must be near-misses.** "Write a fibonacci function" as a negative for a PDF skill tests nothing. The valuable negatives share vocabulary with the skill but need a different tool — adjacent domains, ambiguous phrasings where naive keyword matching would fire.
- Include cases where the skill competes with another skill and should win, and cases where it should lose.

Then loop: run the query set, look at each miss, adjust the description, re-run. Fixes usually take one of three forms — front-load the concrete use case, name the file types/frameworks explicitly, or add an explicit exclusion ("not for X; use Y instead") to kill false positives.

Have the user sign off on the query set before optimizing against it. Optimizing against a bad eval set is how you confidently make a skill worse.

### Anti-patterns

- No baseline arm — you're measuring the model, not the skill.
- Grading only final outputs, never transcripts.
- Adding a clause per failing example until the skill is a list of special cases.
- Obviously-irrelevant negative queries that guarantee a passing score.
- Rewriting the body and the description in the same iteration — you can't attribute the change.

### Iteration checklist

- [ ] Baseline snapshot taken before any edit
- [ ] Both arms spawned in the same turn, same prompt
- [ ] Assertions objective, named descriptively; subjective aspects left to human judgment
- [ ] Transcripts read for wasted work
- [ ] Skill body no longer than last iteration unless a gap forced it
- [ ] 20-query trigger set reviewed and approved before description tuning
- [ ] Only one variable changed per iteration
