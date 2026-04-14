---
name: debugging-react-rendering
description: Diagnoses unnecessary renders, stale closures, memoization mistakes, and state propagation issues in React applications. Use when UI feels slow, renders are noisy, or component updates are confusing.
when_to_use: rerender, useeffect bug, memoization
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Optimizing React Render Cycles

React's declarative nature means rendering is frequent. The skill is knowing *why* a component renders, *what* it renders, and *when* to memoize. Tools: React DevTools Profiler, React.memo, useMemo, useCallback, Server Components in Next.js.

### When to Use

- App slows down after state updates; you need to identify the render culprit
- Parent re-renders child even though props didn't change
- Next.js pages are slow to load or Server Components re-fetch data on every request
- Testing or optimizing bundle or runtime performance

### Decision Framework for React/Next.js/TypeScript

1. **Render is not expensive; reconciliation is.** React can render 1000s of times/sec in dev mode. Profile with DevTools Profiler to find bottlenecks, not guesses.
2. **Server vs. Client.** In Next.js, render on the server (default) to reduce JS on the client. Use `'use client'` only where interactivity is needed (forms, state, hooks).
3. **Memoization is tactical, not universal.** Use `React.memo` on leaf components that receive expensive props; use `useMemo` and `useCallback` only if Profiler shows a bottleneck.
4. **Dependencies matter.** `useMemo(fn, [obj])` with a new object every render defeats the purpose. Use primitive values, stable references, or useMemo the dependency.
5. **Profiler metrics.** "Render duration" is fast; "commit" is what matters. If a component renders 10ms but commits instantly, it's fine. Focus on high-commit times or frequent re-renders.

### Anti-patterns to Avoid

- Wrapping every component in `React.memo` without profiling. It adds overhead and doesn't help if the parent always passes new props.
- Creating callbacks or derived state without `useCallback` or `useMemo`, then passing them to memoized children—defeats memoization.
- Using inline functions or object literals in props; they create new references every render.
- Over-splitting components. A component that only re-renders when its own state changes is already optimized; splitting it adds indirection.
- Server Components fetching data in a loop instead of batch-loading; causes waterfalls in Next.js.

### Checklist

- [ ] Open React DevTools Profiler; record a typical user interaction (scroll, form input, navigation)
- [ ] Identify components with high render counts or long commit times
- [ ] Check if parent is passing new props (inline functions, object literals) each render
- [ ] If needed, wrap the leaf component in `React.memo` and verify Profiler shows fewer renders
- [ ] For expensive computations, add `useMemo` with stable dependency arrays
- [ ] Test in production mode (Next.js: `npm run build && npm start`), not dev
- [ ] For Next.js: verify data fetching happens in Server Components, not `useEffect` in Client Components
- [ ] Measure: before optimization, profile result, verify improvement

### Worked Example: Memoizing a List Item

```tsx
// Bad: ListItem re-renders on every parent state change, even if item data is identical
function List({ items, onSelect }) {
  return items.map(item => (
    <ListItem key={item.id} data={item} onSelect={onSelect} />
  ));
}

// Better: memoize ListItem and pass a stable callback
const ListItem = React.memo(({ data, onSelect }) => (
  <button onClick={() => onSelect(data.id)}>{data.name}</button>
));

function List({ items, onSelect }) {
  const memoizedSelect = useCallback(onSelect, [onSelect]);
  return items.map(item => (
    <ListItem key={item.id} data={item} onSelect={memoizedSelect} />
  ));
}
```
