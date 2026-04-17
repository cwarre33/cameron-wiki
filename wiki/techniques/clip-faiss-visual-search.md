---
title: CLIP + FAISS Visual Search Pipeline
type: technique
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/production-systems/sofascope.md, wiki/techniques/persistent-model-loading.md, wiki/models/clip.md, wiki/tools/faiss.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [clip, faiss, visual-search, embeddings, cosine-similarity, image-search]
---

# CLIP + FAISS Visual Search Pipeline

Pattern for production image similarity search: encode images with CLIP, index embeddings with FAISS, retrieve nearest neighbors.

## Pipeline

```
Input Image (Base64)
    → Decode (PIL)          ~10ms
    → CLIP Encoding         ~150ms (GPU) / ~970ms (CPU)
    → FAISS Search           ~5–45ms
    → Metadata Lookup         ~5ms
    ─────────────────────────────
    Total (GPU):           <500ms   ✅
    Total (CPU, cached):   ~1,015ms ✅
    Total (CPU, cold):    ~16,800ms ❌ (model reloads each request)
```

## FAISS index choice: `IndexFlatIP` + L2 normalization

**Key insight:** L2-normalizing all vectors before insertion makes dot product (which `IndexFlatIP` computes) mathematically equivalent to cosine similarity.

```python
# Normalize at index build time
vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
index = faiss.IndexFlatIP(768)
index.add(vectors)

# At query time — normalize query vector too
query = query / np.linalg.norm(query)
distances, indices = index.search(query.reshape(1, -1), k)
```

This avoids `IndexFlatL2` (requires distance inversion to get similarity) and custom cosine implementations. Simple, correct, fast.

## CLIP model: `clip-vit-large-patch14`

- 768-dimensional embeddings
- Strong zero-shot visual similarity — no fine-tuning needed for furniture domain
- Memory footprint: ~2.5GB loaded; triggers Windows paging file errors if virtual memory is insufficient
- Lighter alternative: `clip-vit-base-patch32` (lower quality, lower memory)

See [[wiki/models/clip.md]] for model details.

## Index position = metadata position

**Direct index mapping:** FAISS index position directly maps to the metadata array position. No secondary lookup table needed.

```python
distances, indices = index.search(query_vec, k)
results = [metadata[idx] for idx in indices[0]]  # O(1) lookup
```

## Base64 processing

Accepting Base64-encoded images eliminates file I/O overhead. The service receives JSON via stdin, decodes Base64 → PIL Image in memory, encodes with CLIP, searches FAISS, returns JSON via stdout.

## Production considerations

- **200k products at 768 dims:** ~600MB index in memory — viable with 8GB+ RAM
- **Exact search:** `IndexFlatIP` does exhaustive exact search. For catalogs >1M, consider `IndexIVFFlat` (approximate, faster) or `IndexHNSW` (graph-based ANN)
- **GPU acceleration:** 3–5× CLIP encoding speedup with CUDA; FAISS also has GPU support (`faiss-gpu`)
- **Model lifecycle:** See [[wiki/techniques/persistent-model-loading.md]] — the single most impactful optimization

## Implemented in

[[wiki/production-systems/sofascope.md]] — live pilot at Furnitureland South, 200k product catalog
