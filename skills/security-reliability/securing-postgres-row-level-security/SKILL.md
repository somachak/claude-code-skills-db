---
name: securing-postgres-row-level-security
description: "Designs and reviews Postgres Row Level Security for multi-tenant apps: enabling and forcing RLS, writing policies that are both correct and fast (the select-wrapped auth.uid() pattern), SECURITY DEFINER helper functions with locked-down search_path and revoked EXECUTE, least-privilege role grants, and the indexes RLS policies need. Use when adding tenant isolation, reviewing Supabase/Postgres policies, or debugging slow RLS queries."
when_to_use: Use when implementing or reviewing tenant isolation in Postgres/Supabase, writing or optimizing RLS policies, creating SECURITY DEFINER helpers, or auditing database role privileges.
---

## Postgres Row Level Security

Application-level filtering (`where user_id = $current`) is one forgotten WHERE clause away from a data breach. RLS moves tenant isolation into the database: once enabled, every query against the table is filtered by policy, no matter which code path issued it.

### Enabling Correctly

```sql
alter table orders enable row level security;
alter table orders force row level security;  -- applies to the table owner too

create policy orders_user_policy on orders
  for all
  to authenticated
  using ((select auth.uid()) = user_id);
```

`force` matters: without it, the table owner (often your migration/admin role) silently bypasses every policy. Scope policies to roles (`to authenticated`) so anonymous roles get nothing by default. In non-Supabase Postgres, the equivalent identity source is a session setting: `current_setting('app.current_user_id')::bigint`, set per-connection by the app.

### The Performance Trap Everyone Hits

`using (auth.uid() = user_id)` calls the function **once per row** - on a million-row table that is a million calls. Wrapping it in a scalar subquery makes Postgres evaluate it once and cache it:

```sql
using ((select auth.uid()) = user_id)   -- 100x+ faster on large tables
```

This one-character-class change is the highest-leverage RLS review comment you can make. Pair it with an index on every column a policy references (`create index on orders (user_id)`) - policies are predicates, and unindexed predicates are sequential scans.

### Complex Checks: SECURITY DEFINER Helpers

Team/org membership checks that join other tables belong in a helper function, not inline in the policy. But SECURITY DEFINER functions run with the creator's privileges and bypass RLS on tables they touch, so they need three guardrails:

```sql
create or replace function private.is_team_member(team_id bigint)
returns boolean language sql security definer
set search_path = ''            -- 1. pin search_path against hijacking
as $$
  select exists (
    select 1 from public.team_members
    where team_id = $1 and user_id = (select auth.uid())  -- 2. explicit identity check inside
  );
$$;
revoke execute on function private.is_team_member(bigint)
  from PUBLIC, anon, authenticated, service_role;          -- 3. not directly callable
```

Then the policy is a single indexed lookup: `using ((select private.is_team_member(team_id)))`.

### Least Privilege Around RLS

RLS is not a substitute for grants. The application role should hold only the specific `select`/`insert`/`update` it needs on specific tables - never `grant all on all tables`, never a superuser connection (superusers bypass RLS entirely, and any SQL injection becomes catastrophic). Separate read-only roles for reporting.

### Anti-Patterns

- Enabling RLS without `force` and assuming the owner is covered.
- Per-row function calls in policies (unwrapped `auth.uid()`, `current_setting()`).
- SECURITY DEFINER helpers in an exposed schema, without `set search_path = ''`, or missing the internal identity check.
- Policies referencing unindexed columns.
- Relying on `service_role`/superuser connections in app code "because RLS gets in the way" - that removes the entire control.
- Testing only the happy path: verify as the wrong user and as anon that rows are invisible.

### Review Checklist

- Every multi-tenant table: RLS enabled + forced, policies scoped to roles.
- All policy function calls select-wrapped; all policy columns indexed.
- SECURITY DEFINER helpers: private schema, pinned search_path, revoked EXECUTE, identity check inside.
- App connects as a minimal role; no superuser DSNs outside migrations.
- A test proves cross-tenant reads return zero rows, not an error the app happens to swallow.
