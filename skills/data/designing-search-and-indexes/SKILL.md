---
name: designing-search-and-indexes
description: Designs search schemas, indexing strategies, ranking tradeoffs, and query filters. Use when implementing application search, faceting, vector or lexical retrieval, or hybrid discovery features.
when_to_use: search index, elasticsearch, meilisearch
allowed-tools: Read Grep
---

## Full-Text Search, Elasticsearch, and Query Optimization

Keyword search ("find users by name or bio") requires specialized indexing. Traditional relational indexes don't work for substring or fuzzy matching. Use full-text search engines (Elasticsearch, Meilisearch, typesense) or PostgreSQL full-text search.

### When to Use

- User-facing search (products, posts, people)
- Autocomplete and suggestions
- Filtering and faceted search
- Analytics on search queries

### Decision Framework for PostgreSQL Full-Text or Elasticsearch

1. **PostgreSQL GIN index for full-text search.** `to_tsvector(column)` indexes, `plainto_tsquery(user_input)` queries. Good for small to medium datasets.
2. **Elasticsearch for scale.** 100M+ documents, real-time updates, fuzzy matching, facets. Complexity is worth it at scale.
3. **Meilisearch or Typesense for simplicity.** Better UX (typo tolerance, instant results). Easier ops than Elasticsearch. Good for products, blogs.
4. **Autocomplete uses prefix indexing.** Store all prefixes of a term in index, or use trie structure. Blazing fast at scale.
5. **Relevance tuning is iterative.** Measure: which results do users click? Adjust weights (title weight > description). Use learning-to-rank if available.

### Anti-patterns to Avoid

- LIKE queries on large tables. LIKE '%keyword%' is a sequential scan. Use full-text indexing.
- Ignoring relevance. 500 results, user wants the first 5. Ranking matters.
- Reindexing on every write. Use background jobs to batch reindex.
- No query analytics. Don't know what users search for; can't improve.

### Checklist

- [ ] Full-text search index is configured (PostgreSQL GIN or Elasticsearch)
- [ ] Queries use index (not LIKE), confirmed with EXPLAIN ANALYZE
- [ ] Autocomplete is fast (<50ms response)
- [ ] Search results are relevant (ranked by match score, not insertion order)
- [ ] Query logging captures search terms; analyzed monthly
- [ ] Misspellings are handled (fuzzy match or "did you mean")
- [ ] Faceted search (filters) available if needed
- [ ] Test: search for partial match, typo, synonym; verify results
