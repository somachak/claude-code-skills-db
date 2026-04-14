---
name: building-accessible-ui
description: Reviews interface code for accessibility issues, semantic structure, keyboard behavior, focus management, and interaction risks. Use when building or reviewing component libraries, forms, dialogs, navigation, and responsive interfaces.
when_to_use: accessibility audit, keyboard navigation, aria
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Making Interfaces Usable for Everyone

Accessibility isn't an afterthought—it's part of the component contract. A11y shifts from "will screen readers work?" to "does the keyboard navigation flow match the UI intent?" and "are interactive states semantically clear?"

### When to Use

- Auditing component libraries (shadcn/ui, custom React components)
- Building forms, modals, dialogs, tables, or navigation menus
- Reviewing keyboard trap bugs or focus-loss issues
- Implementing ARIA labels, roles, landmarks for complex UIs

### Decision Framework for React/TypeScript

1. **Semantic HTML first.** Prefer `<button>` over `<div role="button">`. Use `<label>` for form fields, `<nav>` for navigation. Check shadcn/ui component source—it often includes ARIA patterns out of the box.
2. **Focus management.** React doesn't restore focus automatically when content unmounts. Use `useRef` to trap focus in modals; restore it on close. Test with Tab, Shift+Tab, and Escape.
3. **ARIA only when semantic HTML isn't enough.** Don't add `aria-label` to a properly labeled `<input>`. Do use `aria-live` for toast notifications, `aria-expanded` for accordion toggles.
4. **Contrast and spacing.** Tailwind defaults (text-foreground on bg-background) usually meet WCAG AA. Verify color contrast in tools like WebAIM. Ensure touch targets are ≥44×44 CSS pixels.

### Anti-patterns to Avoid

- Using `<div onClick>` for buttons without role, ARIA, or keyboard handlers—screen readers see it as text.
- Hiding focus rings with `outline: none` in CSS without replacing them visually.
- Forgetting `htmlFor` on `<label>` or wrapping unassociated inputs in fieldset/legend.
- Relying solely on color to indicate state (error red, success green) without text or icon.
- Nesting interactive elements (`<button>` inside `<a>`) which confuse keyboard and screen reader users.

### Checklist

- [ ] Inspect semantic structure: headings, landmarks, form groups, list hierarchy
- [ ] Tab through the entire interface; verify focus order matches visual flow
- [ ] Test with a screen reader (NVDA, JAWS, or Mac VoiceOver)
- [ ] Check color contrast (WCAG AA minimum 4.5:1 for text)
- [ ] Verify all interactive elements are keyboard accessible (Enter, Space, Arrow keys as appropriate)
- [ ] Ensure form error messages are associated with inputs via `aria-describedby`
- [ ] Run axe DevTools or Lighthouse a11y audit; fix critical violations

### Worked Example: Accessible Dropdown in React + shadcn/ui

```tsx
// Bad: no keyboard handling, no semantics
<div onClick={() => setOpen(!open)}>
  Menu
  {open && <div>Option 1</div>}
</div>

// Good: uses shadcn Select (which includes ARIA and keyboard)
<Select value={value} onValueChange={setValue}>
  <SelectTrigger aria-label="Choose an option">
    <SelectValue placeholder="Select..." />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="opt1">Option 1</SelectItem>
  </SelectContent>
</Select>
```
