---
name: building-nextjs-shadcn-interfaces
description: "Builds production-grade Next.js 15 + shadcn/ui interfaces: project setup, file organisation, route groups, async params migration, CSS variable theming, and component composition rules. Guides the 'use client' boundary placement, cn() class merging, serialisable props enforcement, and avoidance of generic AI-generated aesthetics. Use when scaffolding a new Next.js project, adding shadcn/ui to an existing one, building complex layouts, or reviewing UI code for App Router compliance. Triggers: shadcn, nextjs ui, next.js components, tailwind component system."
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Next.js 15 + shadcn/ui Interface Builder

Build distinctive, production-grade frontends — not generic AI-slop UIs.

## When to Use
- Scaffolding a new Next.js 15 project with shadcn/ui
- Adding UI components to an existing App Router project
- Reviewing layouts for client-boundary or theming mistakes
- Migrating from a custom component library to shadcn primitives

---

## Project Scaffold

```bash
bunx --bun shadcn@latest init \
  --preset "https://ui.shadcn.com/init?base=radix&style=nova&baseColor=neutral&iconLibrary=lucide&font=geist-sans" \
  --template next
```

This initialises Next.js 15 + shadcn nova style + Geist font + Lucide icons in one command.

---

## File Organisation

```
app/
├── (protected)/         # Routes requiring auth
│   ├── dashboard/
│   └── settings/
├── (public)/            # Unauthenticated routes
│   ├── login/
│   └── register/
├── actions/             # Server Actions (global)
├── api/                 # Route Handlers
├── layout.tsx           # Root layout
└── globals.css          # CSS variable tokens
components/
├── ui/                  # shadcn primitives (auto-generated, don't edit)
└── shared/              # Business components
hooks/                   # Custom React hooks
lib/                     # Shared utilities (cn, auth helpers)
data/                    # Database query functions
ai/                      # AI tools, agents, system prompts
```

Route groups `(protected)` and `(public)` organise auth boundaries without adding URL segments.

---

## Core Composition Rules

### 1. Import Aliases — always `@/`
```tsx
import { Button } from "@/components/ui/button";  // ✅
import { Button } from "../../components/ui/button"; // ❌
```

### 2. Class Merging with `cn()`
```tsx
import { cn } from "@/lib/utils";

function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("rounded-lg border bg-card p-6 shadow-sm", className)} {...props} />
  );
}
```

### 3. Minimal `'use client'` Boundaries
```tsx
// layout.tsx — Server Component, no directive needed
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-[240px_1fr] min-h-screen">
      <Sidebar />          {/* Server Component */}
      <main>{children}</main>
      <ThemeToggle />      {/* Client Component — tiny leaf */}
    </div>
  );
}

// ThemeToggle.tsx — only this file needs 'use client'
"use client";
export function ThemeToggle() {
  const [dark, setDark] = useState(false);
  return <Button onClick={() => setDark(d => !d)}>{dark ? "☀️" : "🌙"}</Button>;
}
```

### 4. CSS Variables — Never Hardcode Colours
```css
/* globals.css — tokens that shadcn themes use */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
}
```
```tsx
// Use semantic tokens, not raw Tailwind colours
<div className="bg-background text-foreground">   {/* ✅ */}
<div className="bg-white text-gray-900">          {/* ❌ — breaks dark mode */}
```

---

## Async Params (Next.js 15+)

```tsx
// app/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;   // Must await in Next.js 15
  return <h1>{slug}</h1>;
}
```

---

## Server Actions in Forms

```tsx
// actions.ts
"use server";
export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;
  await db.insert(posts).values({ title });
  revalidatePath("/posts");
}

// page.tsx — Server Component, no 'use client' needed
export default function NewPostPage() {
  return (
    <form action={createPost}>
      <Input name="title" placeholder="Post title" />
      <Button type="submit">Create</Button>
    </form>
  );
}
```

---

## Design Principles (Avoid Generic AI Output)

- **No purple gradients** — use neutral backgrounds, meaningful colour only for status/CTAs
- **Icons communicate, labels clarify** — don't stack both unless there's a real reason
- **Whitespace is structure** — spacing rhythm should match the design system tokens
- **Every element earns its place** — decoration without function is noise

---

## Common Mistakes Checklist

- [ ] `'use client'` placed at layout level rather than leaf component
- [ ] Hardcoded Tailwind colours instead of CSS variables (`text-gray-900` vs `text-foreground`)
- [ ] Relative imports instead of `@/` alias
- [ ] Async `params` or `searchParams` not awaited (Next.js 15)
- [ ] `onClick` passed from Server Component without Server Action
- [ ] shadcn `ui/` components edited directly (they regenerate on `shadcn add`)
