---
name: verifying-responsive-layouts
description: Checks breakpoint behavior, overflow, spacing collapse, and layout resilience across screen sizes. Use when shipping pages, dashboards, marketing sites, or mobile-heavy workflows.
when_to_use: responsive bug, breakpoints, mobile layout
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Testing Multi-Device Layouts

Responsive design isn't CSS media queries alone—it's testing real devices and viewports, ensuring text is readable, touch targets are large enough, and layouts reflow without breaking. Use Chrome DevTools, real phones, and automated testing.

### When to Use

- After shipping a new page or feature; verify on iOS and Android
- Desktop site works fine but mobile breaks
- Auditing existing responsive behavior
- Planning breakpoint strategy for new components

### Decision Framework for Tailwind + React Components

1. **Test at actual breakpoints.** Tailwind's defaults: sm (640px), md (768px), lg (1024px), xl (1280px). But also test 375px (iPhone SE), 667px (iPhone), 1440px (desktop). Real device sizes, not just designer breakpoints.
2. **Touch targets: ≥44×44 CSS pixels.** Mobile users have fingers, not cursors. Buttons, links, form inputs must be large enough.
3. **Text readability.** Font size should be ≥16px on mobile (prevents zoom on focus). Line-height ≥1.5 for readability.
4. **Reflow, don't hide.** Responsive means content adapts, not disappears. Use `hidden md:block` judiciously; don't hide navigation entirely on mobile.
5. **Container-based responsive.** Newer approach: use container queries (CSS) instead of viewport queries for components that adapt to parent width, not screen width.

### Anti-patterns to Avoid

- Testing only in Chrome DevTools emulator. Real phones behave differently (scroll, reflow, pinch-zoom).
- Using `display: none` for mobile without providing alternative. Users on mobile can still need that content.
- Hard-coding pixel values instead of Tailwind breakpoints. `w-1/2 md:w-1/3 lg:w-1/4` is more maintainable than `width: 50%` + media query.
- Forgetting font size on mobile. `text-sm md:text-base lg:text-lg` ensures readability at all sizes.
- Testing only portrait. Landscape orientation on tablets and phones behaves differently.

### Checklist

- [ ] Test on actual devices: iPhone (portrait & landscape), Android phone, iPad, desktop
- [ ] Verify text is readable without pinch-zoom (font ≥16px, line-height ≥1.5)
- [ ] Check touch targets: buttons, links ≥44×44px
- [ ] Viewport meta tag is set: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] Use Tailwind breakpoints consistently (not custom media queries)
- [ ] Test all breakpoints: 375px, 640px, 768px, 1024px, 1440px
- [ ] Verify images scale appropriately (no pixelation on retina, no overflow on mobile)
- [ ] Ensure navigation is usable on mobile (not hidden, not too crowded)
- [ ] Check dark mode + responsive (if applicable)
- [ ] Lighthouse Mobile score ≥90
