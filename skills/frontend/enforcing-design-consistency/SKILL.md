---
name: enforcing-design-consistency
description: "Keeps AI-built UIs looking designed across screens and sessions: lock design decisions (accent, type scale, spacing, radius, motion) in a committed DESIGN.md with tokens-only enforcement, ban the nameable tells of AI-generated UI (default indigo, emoji icons, even card grids, pure-black backgrounds), and run a score-then-fix loop with rendered visual verification before any screen ships. Use when UI drifts between pages, when output 'looks AI-generated', or when starting a project that must stay visually coherent without a design team."
when_to_use: UI drifts between screens, output looks AI-generated, enforcing design tokens, keeping multi-session frontend work visually coherent
---

## Design Lock: Consistency Enforcement for AI-Built UIs

Creative direction gets an interface to look good once. This skill keeps it looking designed across every screen and session by (1) locking design decisions in the repo, (2) banning the nameable tells of AI-generated UI, and (3) running a score-then-fix loop before any screen ships.

### 1. Lock decisions in a DESIGN.md
At project start (or first UI task), record and commit: accent color (chosen, never defaulted), font pairing, spacing scale, radius scale, shadow ramp, motion durations/easings, and light/dark strategy. Every later UI change reads this file first. Rules:
- **Tokens only.** All values live as CSS variables / Tailwind theme tokens. A hardcoded hex in a component is a bug — it breaks the lock silently on the next screen.
- **Changes are amendments.** Want a new radius? Update DESIGN.md and migrate existing uses; never fork a one-off.
- **One fixed type scale.** Font sizes outside the table are why screens feel "off" without anyone being able to say why.

### 2. Banned on sight — the AI-look tells
Reject these in review regardless of who (or what) wrote them:
- Default indigo `#4F46E5`/`#5E6AD2` accents and purple-gradient-on-white heroes — the universal "an AI made this" signature.
- Emoji as UI icons — random colors, inconsistent cross-OS rendering. Use one icon set at one stroke weight.
- The icon-in-a-chip above every feature card — decoration pretending to be information.
- All-even grids of same-weight centered cards — no focal point is the #1 machine-composed tell. Every screen needs one dominant element.
- Pure `#000` backgrounds — real dark UIs use layered surface ramps (e.g. 900/850/800) with borders from lightened surface, not gray.
- Generic font stacks (Inter/Roboto/system) when the lock specifies a chosen pairing.

Note: banning defaults isn't enough — generation converges on new uniforms. That's why the lock + loop matter more than the list.

### 3. Score-then-fix loop
Before presenting any screen, self-review against the lock and score 0–100 (start at 100, deduct):
- Token violation (hardcoded color/size/radius/shadow): −10 each
- Banned tell present: −15 each
- No clear focal point on the screen: −15
- Type scale drift: −10; spacing off the scale: −5 each
- Motion inconsistent with locked durations/easings: −5

Under 80: fix and re-score before showing anyone. Then **render and look** — open it in the browser or screenshot it. Code-level review misses visual failures (overflow, contrast, awkward wrapping) every time.

### 4. Drift prevention across sessions
- Re-read DESIGN.md at the start of every UI session; state the locked accent/fonts in your plan so drift is visible immediately.
- When extending a screen, sample the existing screen's tokens rather than regenerating from taste.
- On finding two components solving the same problem differently (two button variants, two card paddings), consolidate to one and delete the other — divergence compounds.

### Anti-patterns
- Restyling per screen from fresh "inspiration" — coherence beats novelty after the first screen.
- Keeping the lock in your head or a chat thread instead of the repo.
- Scoring your own work without rendering it.
- Letting a deadline exception ("just this once, inline hex") survive the sprint.

### Checklist
- [ ] DESIGN.md exists, committed, and read before UI work
- [ ] Zero hardcoded colors/sizes/radii in components — tokens only
- [ ] No banned tells; one focal point per screen
- [ ] Score ≥80 after self-review deductions
- [ ] Screen rendered and visually verified before handoff
- [ ] New components checked against existing ones for duplication
