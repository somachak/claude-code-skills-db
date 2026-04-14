---
name: hardening-forms-and-validation
description: Strengthens form UX, validation rules, error states, async submission behavior, and client-server contract alignment. Use when shipping login, checkout, onboarding, profile, or settings forms.
when_to_use: form validation, error states, submit flow
paths: "**/*.tsx, **/*.ts, **/*.jsx, **/*.js"
allowed-tools: Read Grep
---

## Client and Server Form Validation

Forms are the gateway to user data and backend state. Validation happens twice: client-side for UX (instant feedback), server-side for security (untrusted input). In Next.js, use Server Actions with Zod; on the client, shadcn/ui components + react-hook-form.

### When to Use

- Building or reviewing login, sign-up, payment, or data-entry forms
- Adding cross-field validation (password confirmation, date ranges)
- Hardening against XSS, CSRF, or input injection
- Designing error messaging and recovery flows

### Decision Framework for Next.js/React/TypeScript + Zod

1. **Zod schema is the source of truth.** Define validation once in TypeScript (Zod or similar), use it client and server.
2. **Server Actions are default.** In Next.js, forms should POST via Server Action (with CSRF protection built-in), not fetch(). This keeps secrets server-side.
3. **Real-time validation is UX, not security.** Use `onBlur` or debounced `onChange` for instant feedback (e.g., "username already taken"), but don't trust it. Validate again on server.
4. **Field-level error display.** Show errors under the field (via `aria-describedby`), not in a summary. shadcn/ui Form handles this cleanly with react-hook-form integration.
5. **Sanitize HTML; don't strip it.** Use `DOMPurify` or a Zod preprocessor to allow safe markup (if needed), not a blacklist.

### Anti-patterns to Avoid

- Client-side validation only. No amount of JavaScript stops a curl request or a modified Network tab.
- Storing passwords in state or local storage. Use browser password managers and secure cookies.
- Rendering unescaped user input (`<div>{userComment}</div>`). Use `textContent` or sanitize with DOMPurify.
- Double-posting (user clicks Submit, form submits twice). Disable the button or track a `pending` flag during submission.
- Custom validation logic instead of Zod schemas. Maintenance nightmare; Zod is the standard.

### Checklist

- [ ] Define Zod schema for all inputs; use it in both client and server
- [ ] Bind form to react-hook-form; leverage built-in validation
- [ ] Add real-time validation feedback on blur for UX (username, email, etc.)
- [ ] Server Action: validate Zod schema; catch & return errors as form state
- [ ] Display server errors under the respective field via error component
- [ ] Disable Submit button while submission is pending
- [ ] Test: submit form with missing fields, invalid email, XSS payloads (`<img onerror>`)
- [ ] Ensure CSRF token is included (Next.js Server Actions handle this automatically)
- [ ] Check that password fields don't appear in browser history or logs
