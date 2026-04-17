---
title: Persistent Model Loading Pattern
type: technique
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/production-systems/sofascope.md, wiki/techniques/clip-faiss-visual-search.md, wiki/decisions/sofascope-persistent-service-stdin-stdout.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [ml-serving, latency, model-loading, python, production, optimization]
---

# Persistent Model Loading Pattern

**Rule: Load ML models once at service startup. Never reload per request.**

This is the single most common source of catastrophic latency in naive ML serving implementations.

## The problem

Every ML framework loads model weights from disk on instantiation. For large models this takes seconds:

```
CLIP (clip-vit-large-patch14):  ~2,500ms to load
Whisper large-v3:               ~3,000–8,000ms
LLaMA 7B (CPU):                 ~10,000–30,000ms
```

If the model is instantiated inside the request handler, every request pays this cost.

## Before vs. after (SofaScope)

```
BEFORE (model per request):
  Model Loading:    2,737ms
  CLIP Encoding:      150ms
  FAISS Search:        15ms
  API Overhead:    13,876ms
  ─────────────────────────
  Total:           16,783ms  ❌

AFTER (persistent service):
  Model Loading:        0ms  (loaded once at startup)
  CLIP Encoding:      970ms  (CPU) / ~150ms (GPU)
  FAISS Search:        45ms
  ─────────────────────────
  Total:            1,015ms  ✅  (94% improvement)
  With GPU:          <500ms  ✅
```

## Implementation pattern: subprocess stdin/stdout service

One approach (used in SofaScope): run the model as a long-lived subprocess that communicates via stdin/stdout JSON.

```python
# persistent_search_service.py — startup
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")  # once
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
index = faiss.read_index("product.index")  # once
metadata = json.load(open("metadata.json"))  # once

print("SERVICE_READY", flush=True)

# Request loop
for line in sys.stdin:
    request = json.loads(line)
    result = search(request, model, processor, index, metadata)
    print(json.dumps(result), flush=True)
```

The Next.js API layer spawns this process once and pipes requests to it. See [[wiki/decisions/sofascope-persistent-service-stdin-stdout.md]] for why stdin/stdout over HTTP.

## Alternative patterns

| Pattern | When to use |
|---------|-------------|
| **Subprocess stdin/stdout** | Simple, no port management, single-process deployment |
| **FastAPI/Flask server** | Multiple callers, independent scaling, health checks needed |
| **Global variable in worker** | Gunicorn/uvicorn with `--preload` — model loaded in parent process, forked to workers |
| **Model server (TorchServe, Triton)** | High-throughput production, multiple models, GPU batching |

## General rule

Profile first. In SofaScope, the fix was obvious once the per-request timing breakdown was measured — model loading (2,737ms) dwarfed actual inference (165ms). **Always instrument with per-stage timing before optimizing.**

## Related

- [[wiki/production-systems/sofascope.md]] — where this pattern was applied
- [[wiki/techniques/clip-faiss-visual-search.md]] — the pipeline it accelerates
