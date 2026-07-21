---
title: SofaScope — AI-Powered Furniture Visual Search
type: production-system
status: active
visibility: public
sources:
  - raw/repos/sofascope-ai-powered-product-match-finder.md
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
related:
  - wiki/techniques/clip-faiss-visual-search.md
  - wiki/techniques/persistent-model-loading.md
  - wiki/techniques/hybrid-search-routing.md
  - wiki/decisions/sofascope-metadata-vs-embeddings.md
  - wiki/decisions/sofascope-persistent-service-stdin-stdout.md
  - wiki/tools/faiss.md
  - wiki/models/clip.md
  - wiki/interview-prep/system-design-visual-search.md
  - wiki/initiatives/sellsmart-program.md
  - wiki/production-systems/inventory-lookup-clearview.md
created: 2026-04-17
updated: 2026-07-21
confidence: high
tags: [clip, faiss, visual-search, next.js, python, furnitureland-south, production, pilot, flsi-2103]
---

# SofaScope — AI-Powered Furniture Visual Search

Live pilot at Furnitureland South (FLS). Dual-modality search over a **200,000-product catalog**: fast metadata-weighted text search and CLIP + FAISS image similarity search.

Also an image CDN tier for ClearView inventory lookup — see [[production-systems/inventory-lookup-clearview.md]].

## Status refresh (2026-07-21)

| Key | Summary | Status | Notes |
|-----|---------|--------|-------|
| [FLSI-2103](https://furniturelandsouth.atlassian.net/browse/FLSI-2103) | SofaScope 1.01 Version (epic) | **Testing** | Parent epic under FLSI-173 AI initiative; most children Done |
| [FLSI-2593](https://furniturelandsouth.atlassian.net/browse/FLSI-2593) | SofaScope Tweaks | **Ready for Deployment** | Pre-internal-demo polish (Dec 2025 meetup); residual sub-task FLSI-2599 still Backlog |
| [FLSI-2826](https://furniturelandsouth.atlassian.net/browse/FLSI-2826) | Training/Walkthrough Video & Documentation | **Done** | Created for Sydney’s team walkthrough |
| [FLSI-3004](https://furniturelandsouth.atlassian.net/browse/FLSI-3004) | SofaScope Copilot Tool | **Backlog** | Explore exposing SofaScope endpoint as a Copilot Studio tool; also listed under [[initiatives/sellsmart-program.md]] |

**Contradiction note:** April wiki framing (“live pilot”) still matches Jira — epic FLSI-2103 remains **Testing**, not closed Done. FLSI-2593 is ready to ship but not marked Deployed/Done; one tweak sub-task (Familiar Banner, FLSI-2599) is still Backlog.

### FLSI-2593 tweaks (shipped sub-tasks)

Loading screen, alphabetical filters, back-button fix, show price, show location, universal screen-size compatibility — all **Done**. Open: FLSI-2599 Familiar Banner for Design Consultants (**Backlog**).

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
- FLSI-2518 Milvus research (**Done**) explored ANN alternatives; FAISS remains the production index (⚠️ no follow-on migrate ticket in Cameron assignee catalog)

## Related FLSI work (catalog)

Top recent Cameron-touched stories+ from the SofaScope cluster (93 assignee issues total — dense list deferred to period work-log / Task 9). Full freeze: `raw/fls-work/jira/2026-07-21/cluster-map.md` + assignee catalog.

| Key | Summary | Status | Updated |
|-----|---------|--------|---------|
| [FLSI-2593](https://furniturelandsouth.atlassian.net/browse/FLSI-2593) | SofaScope Tweaks | Ready for Deployment | 2026-06-29 |
| [FLSI-2410](https://furniturelandsouth.atlassian.net/browse/FLSI-2410) | Get FLSI-2321-Build-Containers Branch up-to-date | Done | 2026-06-29 |
| [FLSI-3004](https://furniturelandsouth.atlassian.net/browse/FLSI-3004) | SofaScope Copilot Tool | Backlog | 2026-04-09 |
| [FLSI-2103](https://furniturelandsouth.atlassian.net/browse/FLSI-2103) | SofaScope 1.01 Version (epic) | Testing | 2026-03-11 |
| [FLSI-2826](https://furniturelandsouth.atlassian.net/browse/FLSI-2826) | Training/Walkthrough Video & Documentation | Done | 2026-02-17 |
| [FLSI-2360](https://furniturelandsouth.atlassian.net/browse/FLSI-2360) | Connect with Marketing on SofaScope Logo | Done | 2026-01-05 |
| [FLSI-2518](https://furniturelandsouth.atlassian.net/browse/FLSI-2518) | Milvus Research | Done | 2025-11-19 |
| [FLSI-1489](https://furniturelandsouth.atlassian.net/browse/FLSI-1489) | AI-Powered Product Match Finder (intern epic) | Done | 2025-07-28 |

Adjacent epic still open in cluster: [FLSI-2061](https://furniturelandsouth.atlassian.net/browse/FLSI-2061) Update Image Color/Material Classifier (**Backlog**); child integrate story FLSI-2232 **Closed**.

## Interview angles

This system demonstrates: latency profiling (finding model reload as root cause), hybrid search architecture decisions, production ML serving patterns, and cost-conscious design (zero embedding API costs for text search). See [[wiki/interview-prep/system-design-visual-search.md]].
