---
title: System Design — Visual Search at Scale (SofaScope)
type: interview-note
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/production-systems/sofascope.md, wiki/techniques/clip-faiss-visual-search.md, wiki/techniques/persistent-model-loading.md, wiki/decisions/sofascope-metadata-vs-embeddings.md, wiki/decisions/sofascope-persistent-service-stdin-stdout.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [interview, system-design, visual-search, ml-serving, faiss, clip]
---

# System Design — Visual Search at Scale (SofaScope)

Interview preparation grounded in real production work at FLS.

## The story (behavioral framing)

"I built an AI-powered visual search system for a 200,000-product furniture catalog. Initial image search was taking 16+ seconds — completely unusable. I profiled the pipeline, found that 99% of the latency was model loading per request (not inference), and redesigned the service to keep the CLIP model resident in memory. Result: 16.8s → <500ms, now live as a production pilot."

## Key technical talking points

### 1. Profiling-first diagnosis
The naive assumption would be "CLIP is slow, optimize CLIP." Per-stage timing revealed the real bottleneck: model loading (2,737ms) dwarfed encoding (150ms) by 18×. **The lesson: measure before you optimize.**

### 2. Choosing the right search architecture per modality
- Text: metadata scoring (45ms, zero cost, 92% accuracy) — embeddings were overkill for structured furniture attributes
- Image: CLIP + FAISS (can't express visual similarity as rules)
- Insight: "more ML" is not always the right answer; domain structure matters

### 3. FAISS index design
- `IndexFlatIP` + L2 normalization = cosine similarity (clean, no postprocessing)
- Direct index-to-metadata mapping eliminates secondary lookups
- At 200k × 768 dims: ~600MB, exact search viable; discuss ANN alternatives for scale

### 4. IPC pattern tradeoffs
- Chose stdin/stdout subprocess over HTTP for single-caller pilot deployment
- Discussed when to migrate: multiple callers, independent scaling, batching needs

## Follow-up questions to anticipate

**"How would you scale this to 10M products?"**
→ Switch `IndexFlatIP` to `IndexIVFFlat` (approximate, cluster-based). Train with `nlist=4096`. Set `nprobe=64` for accuracy/speed tradeoff. Consider `IndexHNSW` for low-latency ANN. Move Python service to dedicated FastAPI with GPU workers.

**"How would you handle image quality variation in user uploads?"**
→ CLIP is robust to moderate quality variation. For very low quality: preprocessing pipeline (resize, normalize). Could add a quality gate before embedding.

**"What would you do differently?"**
→ Start with the persistent service pattern from day one. The per-request model loading was a classic rookie mistake that's well-documented — should have profiled immediately when first testing. Also: `IndexIVFFlat` from the start for a 200k catalog (exact search works but sets a bad precedent for growth).

**"How do you evaluate search quality?"**
→ Text: manually curated query-result pairs, success rate metric. Image: user click-through rate on returned results. Currently 85%+ visual similarity accuracy by manual spot-checking.

## Resume bullet (sanitized)

> Built CLIP + FAISS visual similarity search over a 200k-product catalog; diagnosed 16.8s latency root cause as per-request model reloading; redesigned as persistent service, achieving >94% latency reduction (<500ms) in production pilot
