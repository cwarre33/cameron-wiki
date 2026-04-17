---
title: FAISS — Facebook AI Similarity Search
type: tool
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/techniques/clip-faiss-visual-search.md, wiki/production-systems/sofascope.md, wiki/models/clip.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [faiss, vector-search, similarity-search, embeddings, ann, meta]
---

# FAISS — Facebook AI Similarity Search

Meta's library for efficient similarity search and clustering of dense vectors. Core infrastructure for any embedding-based retrieval system.

## Key index types

| Index | Search type | Speed | Accuracy | Memory | When to use |
|-------|------------|-------|----------|--------|-------------|
| `IndexFlatL2` | Exact, L2 distance | Slow at scale | 100% | High | Small datasets, baseline |
| `IndexFlatIP` | Exact, inner product | Slow at scale | 100% | High | Small/medium datasets with normalized vectors |
| `IndexIVFFlat` | Approximate, clustering | Fast | High | Medium | >100k vectors |
| `IndexHNSW` | Approximate, graph | Fast | High | High | Low-latency ANN |
| `IndexPQ` | Approximate, quantized | Very fast | Medium | Low | Huge datasets, memory-constrained |

## Cosine similarity trick with `IndexFlatIP`

**L2-normalize vectors → dot product = cosine similarity.**

```python
vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
index = faiss.IndexFlatIP(dim)
index.add(vectors)

# At query time:
query = query / np.linalg.norm(query)
D, I = index.search(query.reshape(1, -1), k)
# D = cosine similarity scores, I = indices
```

Avoids the complexity of L2-to-cosine conversion. Used in [[wiki/production-systems/sofascope.md]].

## Direct index-to-metadata mapping

Build your metadata array in the same order as you add vectors:

```python
metadata = [product_0, product_1, ..., product_n]
index.add(vectors)  # vector[i] corresponds to metadata[i]

# Retrieval:
_, indices = index.search(query_vec, k)
results = [metadata[i] for i in indices[0]]  # O(1) lookup, no join needed
```

## Scale considerations

At 200k vectors × 768 dims (float32): ~600MB in memory for `IndexFlatIP`. Exact search is O(n) — viable at this scale, but monitor query latency as catalog grows.

At >1M vectors: consider `IndexIVFFlat` (train with `nlist=1024` cluster centroids, set `index.nprobe` to tune accuracy/speed tradeoff).

## GPU support

`faiss-gpu` provides significant speedups for both indexing and search. Combined with GPU-accelerated CLIP encoding, enables sub-500ms end-to-end image search.

## Used in

- [[wiki/production-systems/sofascope.md]] — 200k furniture product visual search
