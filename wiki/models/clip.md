---
title: CLIP — Contrastive Language-Image Pretraining
type: model
status: active
visibility: public
sources: [raw/repos/sofascope-ai-powered-product-match-finder.md]
related: [wiki/techniques/clip-faiss-visual-search.md, wiki/production-systems/sofascope.md, wiki/tools/faiss.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [clip, openai, vision-language, embeddings, zero-shot, multimodal]
---

# CLIP — Contrastive Language-Image Pretraining

OpenAI's vision-language model trained to align image and text embeddings in a shared space via contrastive learning. Enables zero-shot visual similarity and cross-modal retrieval without task-specific fine-tuning.

## Key variants

| Model | Embedding dim | Memory | Speed | Notes |
|-------|--------------|--------|-------|-------|
| `clip-vit-base-patch32` | 512 | ~1GB | Fast | Lighter, lower accuracy |
| `clip-vit-base-patch16` | 512 | ~1.5GB | Medium | Better than patch32 |
| `clip-vit-large-patch14` | **768** | **~2.5GB** | Slower | Best quality; used in SofaScope |

## Zero-shot visual similarity

CLIP embeddings capture semantic appearance without domain-specific fine-tuning. For furniture similarity search, the model generalizes well without any FLS-specific training data — visual similarity (style, shape, color) maps naturally to embedding distance.

## Production characteristics (from SofaScope)

- **Encoding latency (GPU):** ~150ms per image
- **Encoding latency (CPU, warm):** ~970ms per image
- **Model loading time:** ~2,500ms (critical: load once, not per request — see [[wiki/techniques/persistent-model-loading.md]])
- **Memory footprint:** ~2.5GB — can trigger Windows paging file errors on <8GB RAM systems
- **Input:** Base64-encoded images (no file I/O required)

## Windows memory note

`clip-vit-large-patch14` requires 8GB+ RAM. On Windows with insufficient virtual memory, loading triggers: `The paging file is too small for this operation to complete (os error 1455)`. Fix: increase Windows virtual memory to 8GB initial / 16GB max, or switch to `clip-vit-base-patch32`.

## Used in

- [[wiki/production-systems/sofascope.md]] — visual similarity search over 200k furniture products
- [[wiki/techniques/clip-faiss-visual-search.md]] — full pipeline documentation
