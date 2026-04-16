---
name: avoiding-nextjs-app-router-anti-patterns
description: "Identifies and fixes common Next.js 14/15 App Router anti-patterns: misuse of useEffect for data fetching or browser detection, incorrect Server/Client component boundaries, unnecessary client-side state, and Pages Router migration mistakes. Use when reviewing Next.js code, debugging hydration errors, detecting waterfall data fetching, or migrating from Pages Router. Covers TypeScript strict mode, async params/searchParams (Next.js 15+), and serializable props rules."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Next.js App Router Anti-Pattern Detector

Identify and fix the most common App Router mistakes before they ship.

## When to Use
- Reviewing Next.js 14/15 code for correctness
- Debugging hydration mismatches or flash-of-wrong-content
- Migrating a Pages Router codebase to App Router
- Preventing unnecessary client-side JavaScript

---

## Anti-Pattern Taxonomy

### 1. Misusing `useEffect` for Browser Detection

**Wrong — causes hydration mismatch and flash of default content:**
```tsx
'use client';
export default function BrowserCheck() {
  const [isSafari, setIsSafari] = useState(false);
  useEffect(() => { setIsSafari(/Safari/.test(navigator.userAgent)); }, []);
  return <div>{isSafari ? 'Unsupported' : 'Welcome'}</div>;
}
```

**Correct — direct detection with SSR guard:**
```tsx
'use client';
export default function BrowserCheck() {
  const isSafari =
    typeof navigator !== 'undefined' &&
    /Safari/.test(navigator.userAgent) &&
    !/Chrome/.test(navigator.userAgent);
  return <div>{isSafari ? 'Unsupported' : 'Welcome'}</div>;
}
```
Rule: detect synchronously in the render body, always guard with `typeof navigator !== 'undefined'`.

---

### 2. Using `useEffect` for Data Fetching in Client Components

**Wrong — creates loading state waterfall, blocks SSR:**
```tsx
'use client';
export default function PostList() {
  const [posts, setPosts] = useState([]);
  useEffect(() => { fetch('/api/posts').then(r => r.json()).then(setPosts); }, []);
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

**Correct — move data to a Server Component:**
```tsx
// app/posts/page.tsx — Server Component, no 'use client'
export default async function PostList() {
  const posts = await db.query('SELECT id, title FROM posts');
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```
Rule: if data doesn't require browser events or real-time updates, fetch in a Server Component.

---

### 3. Wrong `'use client'` Placement — Too High

**Wrong — converts entire subtree to client-side:**
```tsx
'use client'; // ← placed on a layout with many static children
export default function DashboardLayout({ children }) { ... }
```

**Correct — push the boundary down to the interactive leaf:**
```tsx
// DashboardLayout.tsx — Server Component (no directive)
export default function DashboardLayout({ children }) {
  return <section>{children}<ThemeToggle /></section>;
}

// ThemeToggle.tsx — tiny leaf that needs state
'use client';
export function ThemeToggle() { const [dark, setDark] = useState(false); ... }
```

---

### 4. Passing Non-Serialisable Props Across the Boundary

**Wrong — functions and class instances can't cross the server→client boundary:**
```tsx
// Server Component
export default async function Page() {
  const handler = () => console.log('click'); // ← closure on server
  return <Button onClick={handler} />;        // ← Button is 'use client'
}
```

**Correct — use Server Actions for callbacks:**
```tsx
// actions.ts
'use server';
export async function logClick() { console.log('click from server'); }

// page.tsx — Server Component
import { logClick } from './actions';
export default function Page() {
  return <Button onClick={logClick} />;
}
```

---

### 5. `any` Type in TypeScript (Build-Breaking)

```tsx
// Wrong — breaks strict builds
function Page({ params }: { params: any }) { ... }

// Correct — fully typed App Router props
function Page({ params }: { params: { slug: string } }) { ... }
function Page({ searchParams }: {
  searchParams: { [key: string]: string | string[] | undefined }
}) { ... }
async function myAction(formData: FormData) { ... }  // Server Action
```

---

### 6. Async Params / SearchParams (Next.js 15+)

Next.js 15 made `params` and `searchParams` async. Access them with `await` or `use()`:

```tsx
// pages/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  ...
}
```

Run the official codemod if migrating: `npx @next/codemod@canary upgrade latest`.

---

## Decision Checklist

Before opening a PR on Next.js code, verify:

- [ ] No `useEffect` used purely for data fetching (use Server Components or SWR/TanStack)
- [ ] No `useEffect` for synchronous browser detection
- [ ] `'use client'` placed at the smallest possible boundary (leaf, not layout)
- [ ] All props crossing Server→Client boundary are JSON-serialisable
- [ ] No `any` type where specific types are inferrable
- [ ] `params` and `searchParams` awaited in Next.js 15+ projects
- [ ] Browser-only APIs guarded with `typeof window !== 'undefined'`
- [ ] Data fetching in parallel via `Promise.all` where multiple independent fetches exist

---

## Quick Reference: Pages Router → App Router Migration

| Pages Router pattern | App Router replacement |
|----------------------|------------------------|
| `getServerSideProps` | `async` Server Component |
| `getStaticProps` | `async` Server Component + `generateStaticParams` |
| `useRouter().push()` | `useRouter` from `next/navigation` (client only) |
| `_app.tsx` global state | Root `layout.tsx` with context |
| `next/head` | `export const metadata` or `generateMetadata` |
