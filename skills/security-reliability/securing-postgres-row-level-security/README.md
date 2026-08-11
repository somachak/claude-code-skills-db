# Securing Postgres with Row Level Security

**Category:** security-reliability · **Priority:** supporting · **Audience:** full-stack

Designs and reviews Postgres Row Level Security for multi-tenant apps: enabling and forcing RLS, writing policies that are both correct and fast (the select-wrapped auth.uid() pattern), SECURITY DEFINER helper functions with locked-down search_path and revoked EXECUTE, least-privilege role grants, and the indexes RLS policies need. Use when adding tenant isolation, reviewing Supabase/Postgres policies, or debugging slow RLS queries.

## When Claude should reach for this

Trigger phrases: `row level security`, `RLS policy`, `multi-tenant isolation`, `supabase security`, `postgres roles`, `security definer`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
