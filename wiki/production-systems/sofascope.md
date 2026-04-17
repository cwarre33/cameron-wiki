---
title: SofaScope — AI-Powered Furniture Visual Search
type: production-system
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/techniques/clip-faiss-visual-search.md, wiki/techniques/persistent-model-loading.md, wiki/techniques/hybrid-search-routing.md, wiki/decisions/sofascope-metadata-vs-embeddings.md, wiki/decisions/sofascope-persistent-service-stdin-stdout.md, wiki/tools/faiss.md, wiki/models/clip.md, wiki/interview-prep/system-design-visual-search.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [clip, faiss, visual-search, next.js, python, furnitureland-south, production, pilot]
---

# SofaScope — AI-Powered Furniture Visual Search

Live pilot at Furnitureland South (FLS). Dual-modality search over a **200,000-product catalog**: fast metadata-weighted text search and CLIP + FAISS image similarity search.

## Stack

- **Frontend:** Next.js + Tailwind CSS
- **Text search:** Python `DirectMetadataSearcher` — custom field-weighted scoring, LRU cache
- **Image search:** CLIP (`clip-vit-large-patch14`, 768-dim) + FAISS (`IndexFlatIP`) — persistent Python service
- **Routing:** `RealSearchEngine` TypeScript class — auto-routes text vs. image queries with fallback. See [[wiki/techniques/hybrid-search-routing.md]].

## Performance (production, GPU-accelerated)

| Modality | Latency | Accuracy | Notes |
|----------|---------|----------|-------|
| Text search | ~45ms | 92% | Direct metadata, no embeddings |
| Image search | **<500ms** | 85%+ visual similarity | Persistent CLIP model in memory |

Original image search latency: **~16.8s** (model reloaded per request). Fix: persistent service keeps CLIP resident. See [[wiki/techniques/persistent-model-loading.md]].

## Key architectural decisions

1. **Text search uses metadata scoring, not embeddings** — 55× faster, better domain accuracy for structured furniture attributes. See [[wiki/decisions/sofascope-metadata-vs-embeddings.md]].
2. **Persistent service communicates via stdin/stdout, not HTTP** — avoids port management and HTTP overhead at the cost of subprocess dependency. See [[wiki/decisions/sofascope-persistent-service-stdin-stdout.md]].
3. **FAISS `IndexFlatIP` + L2 normalization = cosine similarity** — simpler than `IndexFlatL2` with distance inversion, same semantic result. See [[wiki/techniques/clip-faiss-visual-search.md]].

## Text search field weights

```
Product Type:   10.0 pts   (exact match)
Product Name:    8.0 pts
Vendor Name:     6.0 pts
Style/Material:  3.0 pts each
Color:           2.0 pts
Description:     1.0 pts
```

## API surface

| Endpoint | Method | Notes |
|----------|--------|-------|
| `/api/search/text` | Direct metadata (default) | 45ms avg |
| `/api/search/text-optimized` | Pure metadata, no fallback | |
| `/api/search/image` | Standard FAISS pipeline | fallback |
| `/api/search/image-persistent` | Persistent service (primary) | <500ms |

## Scale

- **200,000 products** in the FLS catalog (⚠️ docs cite "10,000+" — actual production scale is 20× larger)
- FAISS `IndexFlatIP` performs exact nearest-neighbor search; at 200k × 768-dim this is viable but worth monitoring as catalog grows

## Interview angles

This system demonstrates: latency profiling (finding model reload as root cause), hybrid search architecture decisions, production ML serving patterns, and cost-conscious design (zero embedding API costs for text search). See [[wiki/interview-prep/system-design-visual-search.md]].
