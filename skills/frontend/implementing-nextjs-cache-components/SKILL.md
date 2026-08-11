---
name: implementing-nextjs-cache-components
description: "Implements Next.js Cache Components and Partial Prerendering (PPR): the 'use cache' directive, cacheLife() lifetimes, cacheTag() tagging, updateTag()/revalidateTag() invalidation, and static-shell vs streaming-dynamic composition. Use when a Next.js 15/16 project has cacheComponents enabled, when deciding what to cache vs stream through Suspense, or when replacing deprecated segment config like `export const revalidate`."
when_to_use: "Use when writing Server Components or data fetchers in a Next.js project with cacheComponents: true, when caching decisions (cache vs stream) come up, or when migrating off segment-level revalidate/dynamic exports."
---

## Next.js Cache Components

Cache Components shift caching from segment configuration to compositional code. Instead of `export const revalidate = 3600` controlling a whole route, each component or data function declares its own cache behavior with `'use cache'`, and everything else streams dynamically through Suspense. The result is Partial Prerendering: a static shell sent immediately, cached regions filled from the cache, and dynamic regions streamed per-request.

Detect the mode before applying any of this: check `next.config.ts` for `cacheComponents: true`. Without it, these directives are unavailable and classic segment config still applies.

### The Caching Decision, in Order

1. **Does the component fetch data or do I/O?** No: it is a pure component, nothing to decide.
2. **Does it read request context** (`cookies()`, `headers()`, `searchParams`)? No: go to 3. Yes: go to 4.
3. **Is the data identical across users?** Yes: add `'use cache'` plus `cacheTag()` and `cacheLife()`. No: wrap the render in `<Suspense>` and let it stream.
4. **Can the request-specific value be hoisted out as an argument?** Read `cookies()`/`headers()` outside the cached scope and pass the plain value into a `'use cache'` function; wrap the dynamic caller in `<Suspense>`. Only if compliance forbids cross-request sharing, fall back to `'use cache: private'` (experimental) - still inside Suspense.

The one-line rule: `'use cache'` is for data that is the same for everyone; user-specific data stays dynamic and streams.

### Core Pattern: Static + Cached + Dynamic

```tsx
async function FeaturedPosts() {
  'use cache'
  cacheTag('posts')
  cacheLife('hours')
  const posts = await db.posts.findMany({ where: { featured: true } })
  return <PostGrid posts={posts} />
}

export default async function HomePage() {
  return (
    <>
      <Header />                       {/* static shell */}
      <FeaturedPosts />                {/* cached, in shell */}
      <Suspense fallback={<FeedSkeleton />}>
        <PersonalizedFeed />           {/* dynamic, streams */}
      </Suspense>
    </>
  )
}
```

### Invalidation: Tag at Multiple Granularities

Tag cached scopes with both a broad tag and a narrow one (`cacheTag('posts', `post-${id}`)`), then invalidate the narrowest tag that covers the mutation. In Server Actions use `updateTag()` for read-your-own-writes (the user who mutated sees fresh data immediately); use `revalidateTag()` for background freshness where brief staleness is fine. Reusable cached data fetchers (`getUser`, `getPostsByCategory`) belong in `lib/data.ts` with their tags and lifetimes co-located.

### Anti-Patterns

- **Server Actions for data fetching.** `'use server'` functions are mutations only. A `getProducts()` marked `'use server'` becomes a public POST endpoint and skips caching entirely. Fetch in Server Components or `'use cache'` functions.
- **Reading `cookies()` inside `'use cache'`.** Request APIs are unavailable in cached scopes; hoist the value out and pass it as an argument (it becomes part of the cache key).
- **Keeping `export const revalidate` / `dynamic = 'force-static'`** alongside Cache Components. These are the deprecated configuration style; replace with `cacheLife()` and Suspense boundaries.
- **One giant cached page.** Caching the whole page throws away PPR's benefit; cache the shareable regions and let personalization stream.
- **Non-serializable arguments to cached functions.** Arguments form the cache key; pass IDs and scalars, not class instances or closures.

### Review Checklist

- `cacheComponents: true` confirmed before using directives.
- Every `'use cache'` scope has an explicit `cacheLife()` and at least one `cacheTag()`.
- Mutations call `updateTag()` (user-facing) or `revalidateTag()` (background) on the narrowest sufficient tag.
- User-specific reads sit inside `<Suspense>`, not inside cached scopes.
- No `'use server'` functions that only read data.
- Build output shows the expected static shell; unexpected fully-dynamic pages usually mean an unhoisted request API.
