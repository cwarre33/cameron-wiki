---
title: "ADR: Metadata Scoring vs. Embeddings for Text Search (SofaScope)"
type: decision
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/production-systems/sofascope.md, wiki/techniques/hybrid-search-routing.md, wiki/techniques/clip-faiss-visual-search.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [adr, search, embeddings, metadata, cost, latency, furnitureland-south]
---

# ADR: Metadata Scoring vs. Embeddings for Text Search (SofaScope)

## Decision

Use custom field-weighted metadata scoring for text search instead of embedding-based semantic search.

## Context

SofaScope needs to search a 200,000-product furniture catalog by text query. The initial implementation used OpenAI embeddings (text-embedding-ada-002 or similar) for semantic similarity. This produced correct results but was slow and expensive.

The furniture domain has highly structured, categorical attributes: product type, vendor, material, style, color. These are enumerable — not free-form prose.

## Options considered

| Option | Latency | Cost | Accuracy | Tunable |
|--------|---------|------|----------|---------|
| OpenAI embeddings | ~2,500ms | Per-API-call | Good for semantic | No |
| Local embeddings (HuggingFace) | ~500ms | Compute only | Good for semantic | No |
| **Direct metadata scoring** | **45ms** | **Zero** | **92% domain-specific** | **Yes** |

## Decision rationale

1. **55× faster** — 45ms vs ~2,500ms is the difference between instant feel and noticeable lag
2. **Zero ongoing cost** — no embedding API calls; pure in-process computation
3. **Better domain accuracy** — field weighting explicitly encodes the importance hierarchy that embeddings must infer implicitly. "Dining table" should strongly outrank "coffee table" for the query "dining table" even though they're semantically close
4. **Tunable relevance** — weights can be adjusted based on observed search behavior without retraining a model
5. **No external dependency** — text search remains available even if the embedding service is down

## Tradeoffs accepted

- **Loses semantic flexibility** — "sofa" won't match "couch" unless synonyms are explicitly handled in product type mapping
- **Requires category maintenance** — the 15+ product type mappings need updating when new categories are added
- **Not suitable for long-form queries** — works for keyword/short phrase search, not natural language questions

## Field weight design

```
Product Type:   10.0  (most important — narrows to correct category)
Product Name:    8.0  (specific item identity)
Vendor Name:     6.0  (brand search is common)
Style/Material:  3.0  (facet filtering)
Color:           2.0  (facet filtering)
Description:     1.0  (catch-all)
```

## Outcome

- 45ms average response time (vs ~2,500ms)
- 92% search success rate in production pilot
- Zero embedding API costs
- LRU cache (1024 entries, 5min TTL) further reduces compute for repeated queries

## Interview framing

This decision demonstrates: profiling before optimizing, domain knowledge informing architecture, cost-conscious engineering, and the insight that "more ML" is not always the right answer for structured data problems.
