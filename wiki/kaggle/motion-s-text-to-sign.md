---
title: "Motion-S: Text-to-Sign Motion Generation"
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/kaggle/deep-past-akkadian-translation.md]], [[wiki/kaggle/mabe-mouse-behavior.md]], [[wiki/kaggle/google-tunix-hackathon.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [kaggle, nlp, sign-language, tfidf, knn, retrieval, motion-generation]
---

# Motion-S: Text-to-Sign Motion Generation

**Competition:** Motion-S: Hierarchical Text-to-Motion Generation for Sign Language (Signvrse)
**Prize:** Kudos | **Deadline:** 2026-05-10 (active as of 2026-04-17)
**Cameron's rank:** 25 | **Score:** 0.43263 | **Top score:** 0.44241 (~2% below #1)

## What it is

Given a text input, generate sign language motion sequences. A hierarchical generation task — the output is skeletal motion data, not video. Signvrse is building sign language generation infrastructure.

## Cameron's approach

**TF-IDF + kNN retrieval** — a non-generative baseline. Rather than training a motion generation model:
1. Encode text inputs with TF-IDF
2. Retrieve the nearest neighbor from a lookup table of (text → motion) training pairs
3. Return the retrieved motion sequence

**Why this works better than expected:** Sign language has a finite, structured vocabulary. For seen or near-seen phrases, retrieval matches are high quality. TF-IDF captures lexical overlap efficiently. The gap between this simple approach and a learned generative model is surprisingly small.

## Results

| Metric | Value |
|--------|-------|
| Cameron's score | 0.43263 |
| #1 score | 0.44241 |
| Gap to first | ~2.2% |
| Current rank | 25 |

**Rank 25 with TF-IDF + kNN is a strong signal** that the competition baseline is dominated by retrieval, and complex generative models haven't yet separated from well-tuned retrieval.

## Key insight

**Simple retrieval beats complex generation when the output space is structured and the training set covers it.** This is a recurring pattern in NLP competitions — bag-of-words / TF-IDF baselines are harder to beat than they should be. Knowing when to reach for retrieval vs. generation is a practitioner skill.

## Status

Competition still active (closes 2026-05-10). Rank 25 is current standing, not final.

## Related competitions

**Sequence generation cluster:** [[wiki/kaggle/deep-past-akkadian-translation.md]] is the other sequence generation competition — text-to-translation vs. text-to-motion, same retrieval-vs-generation tradeoff question. [[wiki/kaggle/google-tunix-hackathon.md]] also involves structured sequence output (reasoning traces).

**Motion/behavior cluster:** [[wiki/kaggle/mabe-mouse-behavior.md]] is the reverse direction — recognizing behavior from motion sequences rather than generating motion from text. Both involve temporal skeletal/pose data.

## What to try next (if continuing)

- Dense retrieval (sentence embeddings) instead of TF-IDF — may catch semantic similarity that lexical matching misses
- Motion interpolation between top-k retrieved candidates
- Hierarchical generation for unseen phrases where retrieval fails
