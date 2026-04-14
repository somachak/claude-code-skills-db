---
name: designing-rest-apis
description: Designs REST APIs with clear resource boundaries, versioning rules, pagination, idempotency, and error contracts. Use when creating or refactoring HTTP services and public or internal APIs.
when_to_use: rest api, http api, pagination
allowed-tools: Read Grep Bash
---

## RESTful API Design Patterns

REST APIs are contracts: clear endpoints, consistent methods, predictable status codes. In Node.js (Express/NestJS) and Python (FastAPI/Django), the skill is modeling resources, versioning, error handling, and documentation.

### When to Use

- Designing new API endpoints or revamping existing ones
- Reviewing API consistency (method usage, URL structure, status codes)
- Planning versioning strategy
- Writing OpenAPI/Swagger documentation

### Decision Framework for Express/NestJS/FastAPI

1. **Resources, not actions.** Endpoint: `GET /users/:id`, `POST /users`, `PATCH /users/:id`, `DELETE /users/:id`—not `GET /getUser` or `POST /createUser`.
2. **Methods match semantics.** GET (safe, idempotent), POST (create), PUT (replace), PATCH (partial update), DELETE (remove). Use correct methods for caching, idempotency, and client libraries to work.
3. **Status codes are precise.** 200 (success), 201 (created), 204 (no content), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 409 (conflict), 500 (server error). Wrong status codes break client logic.
4. **Consistent error format.** `{ error: "...", code: "...", details: {...} }`. Clients parse and display errors reliably.
5. **Pagination, filtering, sorting via query params.** `GET /users?page=1&limit=10&sort=name&status=active`. Accept operator syntax (e.g., `filter[age][gt]=25`) for complex queries, but keep it simple.
6. **API documentation is required.** Use OpenAPI 3.0 (Swagger). FastAPI and NestJS auto-generate it; Express needs `swagger-jsdoc`.

### Anti-patterns to Avoid

- RPC-style endpoints: `/api/getUserById/:id` instead of `GET /users/:id`. RESTful clients and frameworks rely on standard methods.
- Inconsistent status codes: 200 for errors, 400 for server issues. Breaks error handling.
- Embedding actions in verbs: `POST /users/sendEmail` instead of `POST /users/:id/emails` or `POST /emails` (with userId in body).
- Ignoring versioning until it's a crisis. Plan for `/v1/`, `/v2/` or header versioning from day one.
- Large response payloads. Paginate, allow sparse fieldsets (`?fields=id,name`), or split into separate endpoints.

### Checklist

- [ ] Every resource has standard CRUD endpoints (GET, POST, PATCH, DELETE)
- [ ] Status codes are accurate (201 for creation, 204 for no-content, 409 for conflict)
- [ ] Error responses follow consistent format (shape, field names, error codes)
- [ ] Pagination works: `?page=1&limit=20`; includes total count and next/prev links
- [ ] API is documented in OpenAPI 3.0 (auto-generated or hand-written)
- [ ] Filtering and sorting are query params, not path params
- [ ] Authentication (Bearer token, API key) is consistent across all endpoints
- [ ] Versioning strategy is defined and implemented (path, header, or query)
- [ ] Rate limiting headers are sent (`X-RateLimit-Limit`, `X-RateLimit-Remaining`)
- [ ] No sensitive data in URLs (use POST with body for PII)
