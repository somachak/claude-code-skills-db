---
name: designing-component-systems
description: Designs reusable UI component systems, prop APIs, composition rules, and state boundaries. Use when creating or refactoring design systems, shared UI packages, or component libraries.
when_to_use: component library, design system, props api
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Building Scalable UI Foundations

A component system is a contract: props define behavior, composition rules prevent prop drilling, and documentation ensures consistency. In React with TypeScript and shadcn/ui, the system lives in your component library, not scattered across pages.

### When to Use

- Building or auditing a design system / component library
- Designing new foundational components (Button, Input, Card, Layout)
- Establishing naming, composition, and variant patterns
- Planning a transition from ad-hoc components to a system

### Decision Framework for React/TypeScript + Tailwind

1. **Composition over inheritance.** Prefer smaller, focused components (Button, Badge, Icon) that combine via layout primitives (Flex, Stack, Grid via Tailwind) rather than bloated "Card" with many optional props.
2. **Variant-driven props.** Use TypeScript unions for size, color, intent (e.g., `variant: 'primary' | 'secondary' | 'danger'`). shadcn/ui uses the `class-variance-authority` library to manage this cleanly.
3. **Controlled vs. uncontrolled.** Form inputs should support both; checkboxes can be uncontrolled unless part of a form group. Be explicit in JSDoc.
4. **Limit prop explosion.** If a component has >5 conditional props, it's doing too much. Split it or introduce a compound component pattern.
5. **Accessibility by default.** shadcn/ui includes ARIA. Don't bypass it. Document required props (e.g., `aria-label` on IconButton).

### Anti-patterns to Avoid

- Deeply nested component APIs (Button within Wrapper within Container). Keep it flat.
- Props like `isLoading`, `isError`, `isSuccess`—use a single `state` prop or data-driven rendering.
- Mixing styling concerns: don't accept `className` for every element inside a component. Use composition instead.
- Exporting internal styles or themes as the public API. Separate styling logic from component code.
- Creating a "God Component" that tries to handle all use cases; instead, provide primitives and document patterns.

### Checklist

- [ ] Define component hierarchy and naming conventions (e.g., `Button`, `ButtonGroup`, `ButtonIcon`)
- [ ] Document all props with TypeScript types and JSDoc examples
- [ ] Create Storybook stories or a component gallery showing each variant
- [ ] Test composition: buttons in forms, dropdowns in toolbars, etc.
- [ ] Define color palette (via Tailwind), spacing scale, typography rules
- [ ] Ensure consistent sizing (Button height, padding, line-height) across variants
- [ ] Document accessibility requirements (aria-label, role, keyboard handlers)
- [ ] Version the system; plan deprecation for breaking changes
