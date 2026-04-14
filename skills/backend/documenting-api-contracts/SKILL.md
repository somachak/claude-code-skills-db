---
name: documenting-api-contracts
description: Produces concise API contract documentation, examples, and change notes that stay aligned with code. Use when shipping endpoints, SDKs, integrations, or internal platform surfaces.
when_to_use: openapi, api docs, integration guide
allowed-tools: Read Grep Bash
---

## OpenAPI, Changelog, and Client Generation

API documentation is a contract. OpenAPI 3.0 (Swagger) is the standard. Pair it with a changelog tracking breaking changes, deprecations, and new features. Generated clients (TypeScript, Python) reduce integration friction.

### When to Use

- Launching an API or new endpoints
- Deprecating or breaking endpoints
- Generating client SDKs
- Onboarding consumers

### Decision Framework for Node.js/Python

1. **OpenAPI 3.0 is the standard.** FastAPI and NestJS auto-generate it. Express uses swagger-jsdoc. Use tools like Redocly to validate and lint.
2. **Changelog documents intent.** OpenAPI documents the contract; changelog explains why. "Deprecated GET /users/{id}/friends, use GET /relationships/{id}" helps consumers migrate.
3. **Client generation from OpenAPI.** Use OpenAPI Generator or similar to generate TypeScript, Python, etc. clients. Reduces integration bugs.
4. **Deprecation has a runway.** Announce 6 months ahead. Support old and new versions. Provide migration guide.

### Anti-patterns to Avoid

- No API versioning. Changes break old clients immediately.
- OpenAPI out of date. Docs don't match implementation; trust erodes.
- No deprecation policy. Yanking endpoints without notice breaks production.

### Checklist

- [ ] OpenAPI 3.0 spec is generated and published (Swagger UI or ReDoc)
- [ ] Every endpoint has description, parameters, and example requests/responses
- [ ] Error responses are documented (400, 401, 404, 500, etc.)
- [ ] Changelog tracks breaking changes, deprecations, and new features
- [ ] Deprecation notice includes sunset date and migration path
- [ ] Client SDK is generated from OpenAPI and published (npm, PyPI)
- [ ] API versioning strategy is defined (/v1/, /v2/ or header-based)
- [ ] OpenAPI spec is linted (Redocly, spectral) and validated in CI
