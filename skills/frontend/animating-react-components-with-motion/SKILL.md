---
name: animating-react-components-with-motion
description: "Implements 60fps GPU-accelerated animations in React, Next.js, Svelte, and Astro using Motion.dev (the Framer Motion successor). Covers the animation pattern decision tree (entrance, gesture, scroll, layout), spring physics tuning, stagger orchestration, prefers-reduced-motion accessibility, and performance validation. Use when adding page transitions, scroll reveals, hover interactions, drag gestures, or layout animations. Triggers: motion.dev, framer motion, animation react, scroll reveal, parallax, spring physics, whileHover, whileInView, AnimatePresence."
allowed-tools: [Read, Write, Edit, Bash]
---

# React Animation with Motion.dev

Motion.dev (Framer Motion successor, 10M+ downloads/month) — 60fps GPU-accelerated animations for React, Next.js, Svelte, and Astro.

## When to Use
- Adding entrance animations, scroll reveals, or hover effects
- Building gesture interactions (drag, tap, hover)
- Implementing page or route transitions
- Creating layout animations with shared-element morphing

**Don't use for:** CSS-only transitions, static sites without JS, Vue apps (use `motion-v`), complex SVG/Canvas animations (GSAP is better).

---

## Installation

```bash
npm install motion          # React, Next.js, Svelte, Astro
npm install motion-v        # Vue 3
```

Import path by framework:
- React / Next.js: `import { motion, AnimatePresence } from "motion/react"`
- Svelte / Astro: `import { animate, scroll } from "motion"`

---

## Pattern Decision Tree

```
What should animate?

ENTRANCE (mount / page load)
  → initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}

GESTURE (hover / tap / drag)
  → whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
    transition={{ type: "spring", stiffness: 300, damping: 20 }}
    (spring physics — no explicit duration)

SCROLL (reveal / parallax)
  → whileInView={{ opacity: 1, y: 0 }}
    initial={{ opacity: 0, y: 50 }}
    viewport={{ once: true, amount: 0.3 }}

LAYOUT (reorder / expand)
  → <motion.div layout />          (auto FLIP animation)
    <motion.div layoutId="hero" />  (shared-element morph)
```

---

## Copy-Paste Patterns

### Fade-Up Entrance
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
/>
```

### Staggered List
```tsx
const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.12 } },
};
const item = {
  hidden: { opacity: 0, y: 16 },
  show:   { opacity: 1, y: 0,  transition: { duration: 0.4 } },
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i.id} variants={item}>{i.name}</motion.li>
  ))}
</motion.ul>
```

### Hover Card
```tsx
<motion.div
  whileHover={{ y: -6, boxShadow: "0 16px 32px rgba(0,0,0,0.12)" }}
  transition={{ type: "spring", stiffness: 300, damping: 20 }}
/>
```

### Scroll Reveal
```tsx
<motion.section
  initial={{ opacity: 0, y: 48 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.25 }}
  transition={{ duration: 0.55 }}
/>
```

### Exit Animation (requires AnimatePresence)
```tsx
<AnimatePresence>
  {show && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.96 }}
    />
  )}
</AnimatePresence>
```

---

## Spring Physics Reference

```tsx
// Snappy UI response (buttons, toggles)
transition={{ type: "spring", stiffness: 400, damping: 25 }}

// Natural card lift
transition={{ type: "spring", stiffness: 300, damping: 20 }}

// Slow, weighty entrance
transition={{ type: "spring", stiffness: 120, damping: 18, mass: 1.5 }}
```
Rule: prefer spring over tween for interactive elements — it feels physically grounded.

---

## Accessibility (Required)

```tsx
// Always respect prefers-reduced-motion
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

<motion.div
  animate={{ opacity: 1, y: prefersReduced ? 0 : -8 }}
  transition={prefersReduced ? { duration: 0 } : { duration: 0.5 }}
/>
```
Or use the CSS approach alongside: `@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }`

---

## Performance Rules

| Rule | Why |
|------|-----|
| Animate only `transform` and `opacity` | GPU-composited — no layout recalc |
| Never animate `width`, `height`, `top`, `left` | Triggers layout/paint on every frame |
| Add `will-change: transform` on elements that animate often | Pre-promote to GPU layer |
| Keep `staggerChildren` between 0.05–0.2s | Faster feels snappy; slower feels laggy |
| Use `viewport={{ once: true }}` for scroll reveals | Prevents re-triggering on scroll back |

---

## Anti-Patterns

- `duration: 0.8` on a hover effect — too slow, users feel the UI is unresponsive. Keep hover ≤ 0.3s.
- Animating `height: "auto"` without `layout` prop — use `<motion.div layout>` instead.
- Forgetting `key` prop inside `AnimatePresence` — exit animation won't fire.
- Animating 50+ list items simultaneously without stagger — creates a janky blur of motion.
- Using `useEffect` to trigger animations — use `useAnimation` hook or variants instead.

---

## Checklist

- [ ] Animations use only `transform` / `opacity` properties
- [ ] `prefers-reduced-motion` respected
- [ ] Interactive elements have spring transitions (not tween)
- [ ] Scroll reveals use `viewport={{ once: true }}`
- [ ] Exit animations wrapped in `AnimatePresence` with unique `key`
- [ ] Stagger intervals between 0.08–0.15s for list animations
- [ ] Hover duration ≤ 0.25s
