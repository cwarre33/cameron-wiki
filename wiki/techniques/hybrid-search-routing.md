---
title: Hybrid Search Routing (Text + Image)
type: technique
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/production-systems/sofascope.md, wiki/techniques/clip-faiss-visual-search.md, wiki/decisions/sofascope-metadata-vs-embeddings.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [search, routing, hybrid-search, faiss, embeddings, metadata]
---

# Hybrid Search Routing (Text + Image)

Pattern for multi-modal search: route queries to the optimal search engine based on modality rather than using one unified approach.

## Core insight

**Different query types have fundamentally different optimal implementations.** Forcing a single retrieval strategy (e.g., embeddings for everything) sacrifices performance and accuracy for the modality that doesn't benefit from it.

| Query type | Optimal approach | Why |
|-----------|-----------------|-----|
| Text | Structured metadata scoring | Furniture attributes are enumerable; field weighting outperforms cosine similarity on domain-specific structured data |
| Image | CLIP embeddings + FAISS | Visual similarity cannot be expressed as metadata rules; embeddings capture semantic appearance |

## SofaScope routing logic (`RealSearchEngine`)

```typescript
async search(query: SearchQuery): Promise<SearchResults> {
  if (!query.isImage && config.useDirectMetadata) {
    return this.searchWithDirectMetadata(query)  // 45ms
  }
  if (query.isImage) {
    return this.searchWithPersistentService(query)  // <500ms
      .catch(() => this.searchWithImageEmbeddings(query))  // fallback
  }
  return this.searchWithEmbeddings(query)  // fallback for text
}
```

## Why metadata beats embeddings for structured text search

In domains with well-defined categorical attributes (product type, vendor, material, color), explicit field weighting outperforms semantic embeddings because:

1. **Exact matches are more important than semantic proximity** — "dining table" should score higher than "coffee table" even though they're semantically similar
2. **No embedding API latency or cost** — zero external dependencies
3. **Interpretable and tunable** — field weights can be adjusted based on observed search behavior
4. **Handles catalog structure** — product type pre-filtering reduces search space before scoring

SofaScope result: **55× faster** (45ms vs ~2,500ms) with **92% accuracy** vs embedding approach.

## Fallback chain

```
Image query:
  primary   → /api/search/image-persistent  (persistent CLIP service)
  fallback  → /api/search/image             (standard FAISS pipeline)

Text query:
  primary   → /api/search/text              (direct metadata)
  fallback  → /api/search/text-optimized    (pure metadata)
  fallback  → embedding search              (if config.useDirectMetadata = false)
```

## When to use this pattern

- Multi-modal search (text + image, text + audio, etc.)
- Domain has structured, enumerable attributes (e-commerce, medical records, real estate)
- Cost sensitivity: avoid embedding API calls for queries that don't benefit from them
- Latency requirements differ by query type

## Related

- [[wiki/production-systems/sofascope.md]]
- [[wiki/decisions/sofascope-metadata-vs-embeddings.md]] — the ADR for this decision
- [[wiki/techniques/clip-faiss-visual-search.md]] — the image search half
