---
name: implementing-auth-flows
description: Implements authentication and authorization flows across sessions, tokens, roles, and privileged actions. Use when shipping login, SSO, OAuth, password reset, invitation, or RBAC features.
when_to_use: oauth, sso, session
allowed-tools: Read Grep Bash
---

## Authentication and Authorization Patterns

Authentication (who are you?) and authorization (what can you do?) are bedrock. Implement once, carefully. Use industry-standard flows: OAuth2, OpenID Connect, JWTs or sessions. Don't invent your own crypto.

### When to Use

- Designing login, sign-up, MFA, or logout flows
- Adding OAuth (GitHub, Google, social login)
- Reviewing token generation, storage, and validation
- Planning authorization rules (roles, permissions, ACLs)

### Decision Framework for Node.js/Python + Next.js Server Actions

1. **Use Next.js Auth.js (formerly NextAuth).** It handles OAuth, credentials, sessions, MFA—all vetted, maintained. Don't roll your own.
2. **Sessions vs. JWTs.** Sessions (encrypted httpOnly cookies) are simpler for monoliths. JWTs for distributed systems (microservices, mobile). Both can work in Next.js.
3. **Password hashing must use bcrypt or Argon2.** Never store plaintext. Never hash with SHA-256 without salt.
4. **Tokens have short lifespans.** Access token: 15-30 minutes. Refresh token: days or weeks, stored in httpOnly cookie. Rotate on each use.
5. **MFA is opt-in security.** TOTP (Google Authenticator) or WebAuthn. Store secret in secure storage, not plaintext.

### Anti-patterns to Avoid

- Storing passwords in plaintext or with weak hashing (MD5, even with salt).
- JWTs in localStorage (susceptible to XSS). Use httpOnly cookies for JWTs too.
- No refresh token rotation. Stolen refresh token = infinite session.
- Hardcoding OAuth secrets in source code. Use environment variables, never commit.
- Authorization checks in frontend only. Backend must validate every permission.

### Checklist

- [ ] Use Auth.js or similar framework; don't implement crypto yourself
- [ ] Password hashing uses bcrypt or Argon2 with salt
- [ ] Login session is httpOnly cookie or httpOnly JWT in cookie
- [ ] Tokens have short lifespan (access ≤30min, refresh ≤1 week)
- [ ] Refresh tokens are rotated on use or after set expiry
- [ ] Logout clears token and session server-side
- [ ] OAuth (if used) is implemented via Auth.js or certified SDK
- [ ] MFA (if required) uses TOTP or WebAuthn, not custom schemes
- [ ] Authorization: every endpoint checks user permission server-side
- [ ] CSRF token is validated (Next.js Server Actions handle this)
- [ ] Password reset is secure (token sent via email, expires in 1 hour)
