---
name: reviewing-frontend-security
description: Reviews browser-facing code for XSS, token exposure, unsafe rendering, insecure storage, and client-side trust mistakes. Use when handling user content, auth state, embeds, or rich text.
when_to_use: xss, unsafe html, token storage
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Client-Side Security Hardening

XSS, CSRF, supply-chain attacks, and insecure data handling live in the client. The skill is knowing where to sanitize, where to use HTTPS, where to trust (and where not to), and how to protect user data in storage.

### When to Use

- Reviewing a new feature or public-facing page
- Integrating third-party code (analytics, ads, embeds)
- Handling sensitive data (PII, tokens, payment info)
- Preparing for security audit or penetration testing

### Decision Framework for React/Next.js/TypeScript

1. **Always sanitize user input before rendering.** React escapes by default (`textContent`), but dangerouslySetInnerHTML is... dangerous. Use DOMPurify if you must render HTML.
2. **Don't store secrets in localStorage.** Tokens, API keys, user PII: store in httpOnly cookies (set by server) or sessionStorage (cleared on tab close). Never localStorage.
3. **Content Security Policy (CSP) is your shield.** Set `Content-Security-Policy` headers to block inline scripts, restrict script sources, prevent clickjacking.
4. **CSRF tokens on forms.** Next.js Server Actions include CSRF protection automatically. Fetch-based forms need explicit tokens.
5. **Dependency audit monthly.** Run `npm audit` and `npm outdated`. A compromised package in node_modules compromises the app.

### Anti-patterns to Avoid

- Using `dangerouslySetInnerHTML` without sanitization. Every user comment, user bio, etc. is an XSS vector.
- Storing tokens in localStorage and accessing them client-side. Tokens belong in httpOnly cookies, set by the server.
- Trusting user input for calculations (price, discount). Prices calculated server-side, never client-side.
- Embedding third-party scripts without CSP or subresource integrity (SRI). Ad/analytics SDKs are privilege escalation vectors.
- Not checking `Referer` or origin on form submissions. CSRF: attacker submits form from their domain on your user's behalf.

### Checklist

- [ ] Check all user input rendering: text via textContent, HTML via DOMPurify
- [ ] Verify sensitive data (tokens) is in httpOnly cookies, not localStorage
- [ ] Test CSRF: submit a form from a different origin; it should fail
- [ ] Review third-party scripts (analytics, ads); consider CSP restrictions
- [ ] Ensure all external requests use HTTPS (no mixed content)
- [ ] Set CSP header: block inline scripts, restrict script sources
- [ ] Run `npm audit` and fix high/critical vulnerabilities
- [ ] Test XSS: try `<img src=x onerror="alert('xss')">` in any user input field; should be escaped
- [ ] Verify no secrets in source code (check git history, env files)
- [ ] Use SRI (Subresource Integrity) for external scripts
