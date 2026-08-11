---
name: optimizing-nextjs-seo
description: "Implements and audits SEO in Next.js App Router apps: the Metadata API and generateMetadata, separate viewport export, OG/Twitter image file conventions, app/sitemap.ts and app/robots.ts, canonical URLs and hreflang alternates, JSON-LD structured data with XSS-safe serialization, and current (2026) rich-results reality like the FAQPage deprecation. Use when adding metadata to routes, generating sitemaps, debugging indexing problems, or running a pre-launch SEO audit."
when_to_use: Use when implementing metadata, sitemaps, robots rules, social images, or structured data in a Next.js App Router app, or when auditing a site before launch / diagnosing Search Console indexing issues.
---

## Next.js App Router SEO

SEO in App Router is file-convention driven: `metadata`/`generateMetadata` exports, `app/sitemap.ts`, `app/robots.ts`, and image file conventions replace hand-rolled `<head>` management. The skill is knowing which knobs matter in 2026 and which are cargo cult.

### Metadata Essentials

Root layout: set `metadataBase`, a `title` object with `default` + `template` ('%s | Site'), a compelling description (~150-160 chars is a guideline, not a limit), `openGraph`, `twitter`, `alternates.canonical`, and `robots`. Two rules people miss:

- **`viewport` (with `themeColor`/`colorScheme`) must be a separate export** - inside `metadata` it is silently unsupported.
- **Skip `keywords`** - Google ignores the tag entirely.

Dynamic routes use `generateMetadata({ params }, parent)`. `params` is a Promise - await it. Extend parent OG images via `(await parent).openGraph?.images` rather than clobbering. `fetch()` is memoized between `generateMetadata` and the page; wrap DB/ORM loaders in React's `cache()` to avoid double queries. `notFound()`/`redirect()` work inside `generateMetadata` for missing entities.

### Social Images

Prefer the file convention over URL-syncing: drop `opengraph-image.png` / `twitter-image.png` into a route segment and Next.js emits the full tag set; deeper segments override shallower ones. For dynamic images use `ImageResponse` in `opengraph-image.tsx`. Standard size 1200x630.

### Sitemap and Robots

`app/sitemap.ts` returns entries from your CMS/DB. `lastModified` must be the content's real change date - `new Date()` on every build teaches Google to ignore your lastmod entirely. Omit `changeFrequency` and `priority`; Google ignores both. In `app/robots.ts`: never disallow `/_next/` (crawlers need render-critical CSS/JS), and if you add bot-specific rule groups, repeat all disallows - named groups do not inherit `*` rules (RFC 9309). The non-standard `host` directive is ignored; declare the preferred host with canonicals and 301s.

### JSON-LD

Serialize with XSS protection and render in the component tree:

```tsx
<script type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, '\\u003c') }} />
```

Know the 2026 rich-results landscape: **FAQPage rich results are gone** (fully removed May 2026) - keep the markup only as an AI-search extraction signal. Still productive: Organization, Article, BreadcrumbList, and Product. Product markup is two experiences: product snippets (editorial pages, ratings/pros-cons, no price needed) vs merchant listings (purchasable pages - require `offers` with price + availability; add `shippingDetails` and `hasMerchantReturnPolicy`). Variants use `ProductGroup` with `hasVariant`. Structured data must match visible page content or Google discards it.

### Anti-Patterns

- Viewport/themeColor inside the `metadata` object (silently dropped).
- `new Date()` as blanket `lastModified` in sitemaps.
- Disallowing `/_next/` or `/static/` in robots.
- Duplicating parent OG config in every page instead of the template + file conventions (metadata merging is shallow - nested objects replace, not merge).
- Adding a web app manifest "for SEO" - it is a PWA nicety with zero ranking effect.

### Pre-Launch Audit

- `curl /robots.txt` and `/sitemap.xml` return real content.
- Page source shows correct title/description/canonical per route, one `application/ld+json` per entity.
- OG preview correct in a card validator; images 1200x630.
- Core Web Vitals: check field data via Search Console/PageSpeed Insights - Lighthouse is lab-only and cannot measure INP.
- Search Console: no "Discovered - currently not indexed" pileup; if present, fix internal linking and content depth before touching technical knobs.
