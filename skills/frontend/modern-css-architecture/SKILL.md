---
name: modern-css-architecture
description: Improves CSS architecture, token usage, layout consistency, and responsive styling strategy. Use when refactoring styling systems, Tailwind conventions, CSS modules, or shared UI foundations.
when_to_use: tailwind conventions, css architecture, design tokens
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Tailwind + Component Architecture

CSS architecture in 2026 is about utility-first design systems. Tailwind + shadcn/ui eliminates the need for BEM, OOCSS, or CSS-in-JS for most projects. The skill is knowing when to reach for class-variance-authority (cva), when to use CSS custom properties, and when semantic HTML eliminates the need for classes.

### When to Use

- Setting up Tailwind config for a new project
- Designing a color palette, spacing scale, or type scale
- Reviewing component CSS in React or Next.js
- Migrating from CSS Modules or styled-components to Tailwind
- Hardening responsive and dark-mode behavior

### Decision Framework for Tailwind + shadcn/ui + TypeScript

1. **Tailwind config is the API.** Define colors, spacing, fonts, and breakpoints in `tailwind.config.js`. Don't use hardcoded values in JSX. Use CSS variables for runtime theming (dark mode, user preferences).
2. **cva for variants.** Use class-variance-authority to manage Button sizes, colors, states. It's cleaner than ternary classNames.
3. **Semantic HTML first.** A `<heading>` doesn't need `text-2xl font-bold`; use CSS to style headings globally or via a utility class. Grid layouts prefer CSS Grid, not Tailwind padding hacks.
4. **Dark mode via css variables.** Tailwind supports `dark:` prefix, but use CSS custom properties for custom colors so dark mode works everywhere.
5. **Responsive design is mobile-first.** Tailwind's default breakpoints (sm, md, lg) flow naturally. Test on real devices, not just browser resize.

### Anti-patterns to Avoid

- Hardcoding colors in JSX (`bg-[#FF5733]`). Use semantic tokens from Tailwind config.
- Layering custom CSS selectors on top of Tailwind utilities. Use `@layer` or refactor into a component.
- Abusing `!important` to override Tailwind classes. If you need to override, it's a config problem, not a priority problem.
- Ignoring breakpoints in QA. Responsive means it works at 375px, 768px, 1920px—not just the designer's MacBook.
- Custom CSS-in-JS for simple styles. Tailwind + CSS custom properties handle 95% of use cases without complexity.

### Checklist

- [ ] Tailwind config includes project colors, spacing, fonts, and breakpoints
- [ ] Component Button uses cva for variants (size, color, state); not nested ternaries
- [ ] Dark mode works: toggle theme and check colors adapt via css variables or dark: prefix
- [ ] No hardcoded hex colors in components; all colors reference Tailwind config
- [ ] Responsive: test at 375px (mobile), 768px (tablet), 1440px (desktop)
- [ ] Review a component's className: no bloated utility strings; use composition or extract a utility class
- [ ] Ensure accessibility: focus states visible, text contrast ≥4.5:1, touch targets ≥44×44px
- [ ] Check that print styles work (if needed) via @media print or Tailwind print: utilities
