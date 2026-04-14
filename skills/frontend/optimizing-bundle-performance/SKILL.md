---
name: optimizing-bundle-performance
description: Finds bundle growth, heavy dependencies, route-splitting opportunities, and hydration risks. Use when load time, bundle size, or interaction latency becomes a concern.
when_to_use: bundle size, code splitting, hydration
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Reducing JavaScript to Ship Faster

Bundle size directly impacts First Contentful Paint. The strategy: code-split by route, defer non-critical JS, use dynamic imports, and audit dependencies. Next.js handles much of this, but you need to verify.

### When to Use

- Lighthouse reports slow LCP or large JS
- Adding a new package; need to weigh cost vs. benefit
- Post-launch: monitoring JS bundle growth
- App feels slow on 3G or older devices

### Decision Framework for Next.js/React

1. **Route-level code splitting is default in Next.js.** Each page is its own chunk. Don't use one giant bundle.
2. **dynamic() imports defer non-critical components.** Use `dynamic(() => import('./Heavy'), { ssr: false })` for modals, tabs, or below-the-fold content.
3. **Audit node_modules.** Run `npm ls` or tools like `bundlesize` or `esbuild` analyzer. A single dependency can bloat the bundle by 100KB.
4. **Server Components reduce JS.** In Next.js, fetch data on the server; send HTML, not JSON + JS. Only use `'use client'` where interactivity is needed.
5. **Tree-shaking requires ES modules.** CommonJS dependencies don't tree-shake. Prefer ES module packages or use bundler plugins.

### Anti-patterns to Avoid

- Importing unused dependencies (e.g., `import moment from 'moment'` for one date; use native Date or date-fns with tree-shaking).
- Sending entire libraries for minor utilities. Lodash: 70KB. A few native methods: 0KB.
- Not using dynamic imports for route-dependent code. Every page loads every modal, form, etc.
- Server Rendering and Client Rendering the same component twice (duplication).
- Forgetting to build and measure in production mode. Dev mode includes source maps and unminified code.

### Checklist

- [ ] Run `npm run build; npm run start`; measure Final JS size in DevTools Network tab
- [ ] Use Next.js built-in bundle analyzer (`@next/bundle-analyzer`)
- [ ] Check each top-level dependency: is it necessary? Can a smaller alternative replace it?
- [ ] Verify dynamic imports for non-critical routes (modals, settings, etc.)
- [ ] Test on slow 3G in DevTools; confirm LCP is <2.5s
- [ ] Ensure all routes use Server Components by default; mark only interactive parts with `'use client'`
- [ ] Run Lighthouse; check JS size metric specifically
- [ ] Monitor bundle size in CI/CD (e.g., via bundlesize package)
