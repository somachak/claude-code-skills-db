---
name: implementing-postgres-vector-search
description: "Implements semantic, vector, and hybrid full-text search in PostgreSQL using pgvector and ParadeDB (pg_search). Covers HNSW/IVFFlat index selection, cosine vs L2 distance operators, BM25 + RRF hybrid ranking, halfvec(3072) memory savings, connection pooling, performance tuning, and re-ranking with Cohere. Use when adding similarity search, RAG retrieval, or Elasticsearch-alternative search to a Node/Python/FastAPI backend. Triggers: pgvector, vector search, semantic search, hybrid search, HNSW, BM25, RAG retrieval, ParadeDB, pg_search."
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# PostgreSQL Vector and Hybrid Search

Add semantic, keyword, and hybrid search to any Postgres-backed application.

## When to Use
- Building RAG pipelines that need fast nearest-neighbour retrieval
- Replacing Elasticsearch/OpenSearch with a pure-Postgres solution
- Implementing autocomplete, fuzzy search, or similarity scoring
- Scoring and re-ranking results with cross-encoders or Cohere

---

## Setup

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
  id        SERIAL PRIMARY KEY,
  content   TEXT NOT NULL,
  embedding vector(1536)     -- OpenAI text-embedding-3-small
  -- embedding halfvec(3072) -- text-embedding-3-large, saves ~50% RAM
);
```

Docker quick-start:
```bash
# pgvector only
docker run -d -e POSTGRES_PASSWORD=postgres -p 5432:5432 pgvector/pgvector:pg17

# ParadeDB (pgvector + pg_search + BM25)
docker run -d -e POSTGRES_PASSWORD=postgres -p 5432:5432 paradedb/paradedb:latest
```

---

## Distance Operators

| Operator | Metric | Best for |
|----------|--------|----------|
| `<=>` | Cosine | Normalised text embeddings (most common) |
| `<->` | L2 / Euclidean | Image embeddings, non-normalised vectors |
| `<#>` | Negative inner product | When vectors are pre-normalised (fastest) |

---

## Indexing Decision Tree

```
Row count?
├─ < 10 000  → No index needed (sequential scan is fast enough)
├─ 10k–1M   → HNSW (fast query, larger RAM, no training required)
│              CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
│              WITH (m = 16, ef_construction = 64);
└─ > 1M     → IVFFlat (less RAM, requires training data)
               CREATE INDEX ON docs USING ivfflat (embedding vector_cosine_ops)
               WITH (lists = 100);  -- rule of thumb: sqrt(row_count)
```

**HNSW tuning:**
- `m` (16 default): edges per node — higher = better recall, more RAM
- `ef_construction` (64 default): build-time search depth — higher = slower build, better index
- At query time: `SET hnsw.ef_search = 100;` for recall vs. speed trade-off

---

## Core Query Patterns

```sql
-- Basic semantic search
SELECT id, content, 1 - (embedding <=> $1) AS similarity
FROM documents
ORDER BY embedding <=> $1
LIMIT 10;

-- Filter before vector sort (use WHERE early to reduce candidates)
SELECT id, content
FROM documents
WHERE category = 'tech'
ORDER BY embedding <=> $1
LIMIT 10;

-- Preload index on startup (cold-start optimisation)
SELECT 1 FROM documents ORDER BY embedding <=> $1 LIMIT 1;
```

---

## Hybrid Search: Vector + BM25 with RRF

Reciprocal Rank Fusion combines semantic and keyword scores without normalisation:

```sql
-- Using ParadeDB's pg_search for BM25
WITH semantic AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $1) AS rank
  FROM documents
  ORDER BY embedding <=> $1
  LIMIT 60
),
keyword AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY bm25_score DESC) AS rank
  FROM documents
  WHERE content @@@ $2          -- pg_search BM25 operator
  LIMIT 60
)
SELECT
  COALESCE(s.id, k.id) AS id,
  (COALESCE(1.0 / (60 + s.rank), 0) +
   COALESCE(1.0 / (60 + k.rank), 0)) AS rrf_score
FROM semantic s FULL OUTER JOIN keyword k USING (id)
ORDER BY rrf_score DESC
LIMIT 10;
```

---

## Fuzzy / Trigram Search (No Extension Needed)

```sql
-- Enable pg_trgm
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX ON documents USING gin (content gin_trgm_ops);

-- Similarity threshold query
SELECT id, content, similarity(content, $1) AS score
FROM documents
WHERE similarity(content, $1) > 0.3
ORDER BY score DESC
LIMIT 10;
```

---

## Re-Ranking with External APIs (Cohere)

```typescript
// After retrieving top-40 candidates from Postgres:
const { results } = await cohere.rerank({
  model: 'rerank-v3.5',
  query: userQuery,
  documents: candidates.map(c => c.content),
  topN: 10,
});
const reranked = results.map(r => candidates[r.index]);
```

---

## Performance Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Fetching all rows and filtering in app code | Use `WHERE` + LIMIT in SQL |
| No index on a 100k+ row table | Add HNSW (takes ~2 min, online, no lock) |
| `SELECT *` with 1536-float vector column | `SELECT id, content` — exclude the vector from result |
| Rebuilding index on every deploy | Index persists; only rebuild after bulk inserts |
| Storing full `vector(3072)` when half-precision is enough | Use `halfvec(3072)` to halve RAM |

---

## Checklist

- [ ] Extension created: `CREATE EXTENSION IF NOT EXISTS vector`
- [ ] HNSW index added once row count exceeds 10k
- [ ] Distance operator matches embedding normalisation (`<=>` for cosine is safest default)
- [ ] Query filters applied *before* ORDER BY to reduce scan set
- [ ] `SELECT` explicitly excludes the vector column unless needed
- [ ] Connection pool (PgBouncer / Supabase pooler) used in production
- [ ] Embeddings generated outside transactions; stored in bulk
