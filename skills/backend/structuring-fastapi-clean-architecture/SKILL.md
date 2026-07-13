---
name: structuring-fastapi-clean-architecture
description: Structures a FastAPI service into domain/application/infrastructure/presentation layers so business logic stays transport-agnostic and testable. Use when starting a FastAPI service meant to last, adding a second entry point (queue consumer, scheduled job) beside HTTP, or refactoring a main.py-with-everything app into thin endpoints backed by use cases.
when_to_use: fastapi architecture, structure fastapi project, thin endpoints, use case layer
allowed-tools: Read Grep Bash
---

## FastAPI Clean Architecture

FastAPI makes it trivially easy to put business logic in the route handler — and that is exactly why FastAPI services rot. As soon as a second transport appears (a queue consumer, a scheduled job, an internal RPC), logic that lives in `@router.post` has to be copy-pasted or awkwardly imported. This skill encodes a layered structure that keeps endpoints thin and business logic transport-agnostic, so the same use case runs from HTTP, a NATS consumer, or a cron task without change.

### When to Use

- Starting a new FastAPI service that will outlive a prototype
- A service that already has (or will grow) a second entry point: background worker, message consumer, scheduled job
- Refactoring a `main.py`-with-everything FastAPI app into something testable
- You keep repeating auth, validation, or DB-session wiring in every endpoint

### Layer Boundaries (dependencies point inward)

1. **domain/** — entities, value objects, and repository *protocols* (interfaces). Zero imports from FastAPI, SQLAlchemy, or Pydantic. Pure Python.
2. **application/** — use cases: one class per business operation with an `execute()` method. Depends only on domain protocols. Returns domain objects or a `Result`, never a `Response`.
3. **infrastructure/** — concrete adapters: SQLAlchemy repositories, HTTP clients, message publishers. Implements the domain protocols.
4. **presentation/** — FastAPI routers, Pydantic request/response schemas, dependency wiring. Translates transport input into a use case call and the result back into a `Response`. The only layer that imports FastAPI.

The one pragmatic exception worth documenting: `application/` may import the DB session type for transaction control. Everything else stays strictly inward.

### Decision Framework

1. **Endpoints translate, never decide.** A handler parses the request schema, calls one use case, and serializes the result. If a handler contains an `if` about business rules, that logic belongs in `application/`.
2. **One use case = one operation.** `RegisterUser`, `PublishArticle`, `CancelSubscription`. Constructor takes repositories/services (injected); `execute(command)` does the work. This is the unit your queue consumer and cron job also call.
3. **Depend on protocols, inject implementations.** Define `class UserRepository(Protocol)` in `domain/`; the SQLAlchemy version lives in `infrastructure/`. Use cases accept the protocol, so unit tests pass a fake and integration tests pass the real one.
4. **Wire dependencies once, at the edge.** Use FastAPI `Depends` (or a DI container like `dishka`) to build repositories and use cases. Attach auth at the *router* level (`APIRouter(dependencies=[Depends(require_user)])`), grouping routers by audience (`public/`, `user/`, `admin/`) so it is structurally impossible to forget auth on an endpoint.
5. **Async all the way down.** `async def` handlers, `AsyncSession`, `httpx.AsyncClient`. A single sync `requests.get` or blocking DB driver in a handler stalls the event loop for every concurrent request.

### Anti-patterns

| Avoid | Use Instead |
|-------|-------------|
| Business logic inside `@router.post` | A use case in `application/`, called by the handler |
| Importing `Session`/SQLAlchemy models in a router | Repository protocol injected into the use case |
| Returning ORM models directly from endpoints | Explicit Pydantic response schema |
| Re-adding `Depends(get_current_user)` on every route | Router-level `dependencies=[...]`, grouped by audience |
| `requests`/`psycopg2` (sync) in an async handler | `httpx.AsyncClient` / `asyncpg` + `AsyncSession` |
| Catching `Exception` in the handler to shape errors | Domain exceptions + one `exception_handler` per type |
| Testing only through the HTTP layer | Unit-test use cases directly; reserve HTTP tests for wiring |

### Worked Example — a use case reused across transports

```python
# domain/repositories.py
class UserRepository(Protocol):
    async def by_email(self, email: str) -> User | None: ...
    async def add(self, user: User) -> None: ...

# application/register_user.py
@dataclass
class RegisterUser:
    users: UserRepository
    hasher: PasswordHasher
    async def execute(self, cmd: RegisterCommand) -> User:
        if await self.users.by_email(cmd.email):
            raise EmailAlreadyUsed(cmd.email)
        user = User.new(cmd.email, self.hasher.hash(cmd.password))
        await self.users.add(user)
        return user

# presentation/http/users.py  (thin — translate only)
@router.post("/users", response_model=UserOut, status_code=201)
async def register(body: RegisterIn, uc: RegisterUser = Depends(get_register_user)):
    user = await uc.execute(body.to_command())
    return UserOut.from_domain(user)

# the SAME use case, driven by a message consumer
async def on_signup_event(evt: SignupEvent, uc: RegisterUser):
    await uc.execute(evt.to_command())   # zero duplicated logic
```

### Testing Layers

- **Unit** — instantiate the use case with fake repositories; assert domain behavior. No FastAPI, no DB. Fast, covers business rules.
- **Integration** — real SQLAlchemy repository against a `testcontainers` Postgres; verify the adapter honors the protocol.
- **E2E** — drive the app with `httpx.AsyncClient(transport=ASGITransport(app=app))`; assert status codes and wiring, not business branches.

### Checklist

- [ ] No SQLAlchemy or FastAPI imports in `domain/` or `application/`
- [ ] Every endpoint calls exactly one use case and returns an explicit response schema
- [ ] Repositories are defined as protocols in `domain/`, implemented in `infrastructure/`
- [ ] Auth is wired at the router level, routers grouped by audience
- [ ] All I/O is async; no sync HTTP/DB drivers in handlers
- [ ] Domain exceptions map to HTTP via `@app.exception_handler`, not per-route try/except
- [ ] Use cases have direct unit tests; `testcontainers` covers the repository adapters
