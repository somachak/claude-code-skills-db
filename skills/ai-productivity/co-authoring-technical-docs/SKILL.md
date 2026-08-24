---
name: co-authoring-technical-docs
description: "Runs a three-stage workflow for design docs, RFCs, ADRs, PRDs and postmortems: structured context transfer with numbered clarifying questions, section-by-section drafting with decision-first ordering and evidence discipline, then a blind reader test where a fresh zero-context Claude session summarizes the doc and lists what it would need before approving. Use when starting a substantial written artifact that other people must act on, when a draft keeps getting the same review questions, or before sending a doc for approval."
when_to_use: Use when writing or reviewing a design doc, RFC, ADR, PRD, migration plan, or postmortem — especially before it goes to reviewers. Skip for READMEs, changelogs, and anything under a page.
---

## Co-Authoring Technical Docs

Most bad design docs fail the same way: the author knows twenty things the reader doesn't, and only writes down three of them. This is a three-stage workflow for closing that gap — context transfer, structured drafting, then a blind reader test that catches what neither of you can see anymore.

Use it for design docs, RFCs, ADRs, PRDs, incident postmortems, and migration plans. Skip it for READMEs, changelogs, and anything under a page.

### Stage 1 — Context transfer (do not skip to drafting)

Open with five meta questions, answerable in shorthand:

1. Doc type and template, if any?
2. Primary audience — and what do they already know?
3. What should be true after they read it? (approval, alignment, a decision reversal)
4. What decision is actually being made here?
5. Constraints: deadline, prior art, political landmines?

Then ask for an unstructured dump — background, why the obvious alternative was rejected, past incidents, team dynamics, timeline pressure, architecture dependencies, stakeholder objections. Explicitly tell them not to organize it.

**Then ask 5–10 numbered clarifying questions** targeting gaps. Numbering matters: it lets them reply "1: yes, 2: see #eng-platform, 3: no, breaks backcompat" in thirty seconds. Good questions probe for what a skeptical reader will attack:

- What breaks if we do nothing?
- Who has to change their workflow, and have they agreed?
- What's the rollback if this is wrong?
- Which number in here is a guess?

Anti-pattern: asking questions you can answer by reading the repo. Read first, ask second.

### Stage 2 — Structure, then fill

Agree the section list **before** writing prose. A default that works for engineering decisions:

```
Problem            — observable symptoms, with numbers
Context            — what a newcomer needs, nothing more
Options considered — including "do nothing", with why each was dropped
Proposal           — the decision, stated in one sentence up top
Consequences       — what gets worse, not just what gets better
Rollout & rollback — sequencing, flags, kill switch
Open questions     — explicitly unresolved, with owners
```

Draft section by section, not the whole doc at once. After each: ask whether the reasoning matches their intent, then move on. Whole-doc drafts invite whole-doc rewrites.

Two rules that do most of the work:

- **Decision first, reasoning second.** Readers skim. If the proposal appears on page three, half your audience never finds it.
- **Every claim gets a number, a link, or an explicit "unknown".** "Slow queries" is unactionable; "p99 at 4.2s, budget is 800ms" is a mandate. Marking a guess as a guess is what buys the doc credibility.

### Stage 3 — The blind reader test

This is the stage people skip and the one that pays. Hand the finished doc to a **fresh Claude session with zero prior context** — the closest available proxy for a reviewer who wasn't in any of your meetings. Ask it, in a separate conversation:

1. Summarize this doc in three sentences.
2. What decision is being proposed, and what are the alternatives?
3. What questions would you need answered before approving?
4. Where does the reasoning have a gap?

Read the summary first. If it doesn't match your intent, the doc is unclear — not the reader. Questions in (3) that you thought were already answered mark the exact paragraphs to rewrite. Do this before human review, not after: reviewers spend their attention budget once.

Practical note: if the doc contains diagrams or screenshots without alt text, the blind reader is flying half-blind — and so is every future colleague who pastes the doc into an AI tool. Write alt text for anything load-bearing.

### Anti-patterns

- **Drafting during Stage 1.** Producing prose before the dump means the doc anchors on your first guess.
- **Burying the decision** under a history lesson.
- **Fake precision** — "roughly 40% faster" with no benchmark is worse than "unmeasured; we expect a large win."
- **No "do nothing" option.** A doc that never considered the status quo reads as advocacy, not analysis.
- **Open questions with no owner.** They become nobody's problem the moment the doc is approved.

### Ship checklist

- [ ] Decision stated in the first paragraph
- [ ] "Do nothing" evaluated with a real cost attached
- [ ] Every number has a source or is labeled a guess
- [ ] Consequences section names something that gets worse
- [ ] Rollback path exists and is specific
- [ ] Blind-reader summary matches your intent
- [ ] Open questions each have a named owner
