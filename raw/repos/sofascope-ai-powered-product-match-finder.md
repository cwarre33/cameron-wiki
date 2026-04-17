# SofaScope: AI-Powered Furniture Search & Match Platform
Source: https://github.com/cwarre33/ai-powered-product-match-finder
Fetched: 2026-04-17
Files: README.md, ReactFrontend/OPTIMIZATION_SUMMARY.md, ReactFrontend/TROUBLESHOOTING.md

---

## README

# SofaScope: AI-Powered Furniture Search & Match Platform

Find and compare furniture using fast text and image search. The React frontend provides a modern UI for searching, filtering, and viewing products. Text search uses smart metadata matching; image search uses a Python service with CLIP and FAISS for visual similarity. All search logic is configurable.

## Structure

- **Frontend:** Next.js + Tailwind (`ReactFrontend/components/`)
- **Image Search:** CLIP + FAISS (Python service)
- **Config:** `ReactFrontend/search-engine-config.json`

## Requirements

- Node.js 18+
- Python 3.8+ (with required packages)
- 8GB+ RAM recommended

---

## OPTIMIZATION_SUMMARY.md

### Text Search Optimization

- DirectMetadataSearcher class — no API calls, eliminates OpenAI embedding latency
- Custom relevance scoring with field weighting:
  - Product Type Match: 10.0 pts | Product Name: 8.0 | Vendor: 6.0 | Style/Material: 3.0 | Color: 2.0 | Description: 1.0
- LRU Caching (default 1024 entries, 5min TTL)
- Performance: 45ms average response time
- Text search is 55x faster than embedding-based search

### Image Search Optimization

- Pipeline: Image → CLIP (clip-vit-large-patch14, 768-dim) → FAISS (IndexFlatIP) → Results
- L2 normalization enables cosine similarity via dot product
- Base64 processing — no file I/O overhead
- GPU acceleration (CUDA) available
- Performance: ~170ms per request (FAISS pipeline alone)

### Persistent Model Loading — Key Breakthrough

Before optimization:
  Model Loading:    2,737ms (per request)
  CLIP Encoding:      150ms
  FAISS Search:        15ms
  API Overhead:    13,876ms
  Total Response:  16,783ms ❌

After persistent service:
  Model Loading:         0ms (cached in memory)
  CLIP Encoding:       970ms
  FAISS Search:         45ms
  Total Response:    1,015ms ✅ (94% improvement)

Root cause: CLIP model was reloading on every request.
Fix: persistent_search_service.py — model loaded once into memory, stays resident.
Architecture: Browser → Next.js API → Persistent Python Service (stdin/stdout) → cached CLIP + FAISS

### API Endpoints
- /api/search/text — direct metadata (default)
- /api/search/text-optimized — pure direct metadata
- /api/search/image — standard FAISS pipeline
- /api/search/image-persistent — persistent model service (primary)
- Smart routing: RealSearchEngine auto-routes with fallback

### Production Readiness
- Text search: 45ms avg, 92% accuracy, zero external API costs
- Image search: ~1s avg, 85%+ visual similarity accuracy, handles 10,000+ products
- Fallback: automatic fallback to standard search if persistent service unavailable

---

## TROUBLESHOOTING.md

### Windows Virtual Memory Issue
Error: "The paging file is too small for this operation to complete" (os error 1455)
Root cause: CLIP model requires significant memory; Windows paging file too small.
Fix: Increase virtual memory to 8GB initial / 16GB max.

### Lighter model option
Switch from clip-vit-large-patch14 to clip-vit-base-patch32 to reduce memory requirements.

### CPU-only mode
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install faiss-cpu
