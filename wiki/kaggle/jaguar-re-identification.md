---
title: Jaguar Re-Identification Challenge
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/production-systems/sofascope.md]], [[wiki/techniques/clip-faiss-visual-search.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, computer-vision, re-identification, wildlife, metric-learning]
---

# Jaguar Re-Identification Challenge

**Competition:** Jaguar Re-Identification Challenge
**Prize:** Kudos | **Deadline:** 2026-03-14 (closed)
**Cameron's rank:** Outside top 200 | **Top score:** 0.979

## What it is

Re-identify individual jaguars from camera trap images. Given multiple photos of jaguars, determine which images show the same individual. Wildlife conservation application — automated individual tracking without physical tagging.

## Domain context

Re-identification is a metric learning problem: learn an embedding space where images of the same individual cluster together and images of different individuals separate. Standard approaches:
- Contrastive or triplet loss training
- ArcFace / CosFace for learned similarity
- CLIP-style vision encoders as backbone
- Test-time augmentation + re-ranking

Connects to Cameron's CLIP+FAISS work in [[wiki/production-systems/sofascope.md]] — same embedding-retrieval paradigm, different domain. See [[wiki/techniques/clip-faiss-visual-search.md]] for the full pipeline.

⚠️ *Stub — rank, score, and approach not confirmed from API data.*
