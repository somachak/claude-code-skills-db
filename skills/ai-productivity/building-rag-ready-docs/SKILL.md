---
name: building-rag-ready-docs
description: Restructures documentation for retrieval quality with chunk-friendly sections, explicit metadata, and stable terminology. Use when preparing codebase docs, runbooks, or API guides for AI systems.
when_to_use: rag docs, retrieval, chunking
---

## Documentation for AI Integration

RAG (Retrieval-Augmented Generation) systems fetch relevant docs to answer questions. Good RAG docs are searchable, structured, and comprehensive. The skill is organizing documentation so AI can retrieve and use it.

### When to Use

- Building a chatbot or AI assistant
- Existing docs are disorganized or scattered
- Need to enable AI to answer codebase questions

### Decision Framework

1. **Structure for retrieval.** Docs are chunked by topic (API endpoints, configuration options). AI can retrieve relevant chunks.
2. **Headings are descriptive.** "Authentication" is vague; "JWT Token Rotation and Expiry" is specific. Improves retrieval relevance.
3. **Examples are concrete.** Code snippets, curl requests, expected responses. AI can extract and reuse.
4. **Cross-references are links.** Markdown links to related docs. Helps AI navigate.
5. **Metadata helps indexing.** Tags (frontend, backend, security) or categories. Narrows search space.

### Anti-patterns to Avoid

- Unstructured docs. Walls of text. Hard to retrieve relevant section.
- No examples. AI doesn't know how to use API or config.
- Scattered docs. README, wiki, Notion, wiki.js—docs everywhere. AI doesn't know where to look.

### Checklist

- [ ] Docs are organized by topic (API, config, deployment, troubleshooting)
- [ ] Each doc has descriptive headings (not generic)
- [ ] Examples are included (code snippets, curl requests, expected output)
- [ ] Docs are linked (cross-references via markdown)
- [ ] Docs are searchable (indexed in RAG system)
- [ ] Metadata (tags, categories) helps retrieval
- [ ] Docs are up-to-date (reviewed quarterly)
- [ ] AI can retrieve and accurately answer questions using docs
