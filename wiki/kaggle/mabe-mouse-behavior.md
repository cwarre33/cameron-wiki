---
title: MABe — Social Action Recognition in Mice
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/kaggle/motion-s-text-to-sign.md]], [[wiki/kaggle/jaguar-re-identification.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, computer-vision, action-recognition, behavioral-analysis, video, neuroscience]
---

# MABe — Social Action Recognition in Mice

**Competition:** MABe Challenge - Social Action Recognition in Mice
**Prize:** $50,000 | **Deadline:** 2025-12-15 (closed)
**Cameron's rank:** Outside top 200 | **Top score:** 0.57473

## What it is

Classify social behaviors (grooming, chasing, mounting, etc.) from video of interacting mice. Neuroscience and behavioral biology application — automated ethology for drug trials and neurological research.

## Domain context

Multi-label temporal classification on pose/keypoint sequences or raw video. The input is typically tracked body keypoints over time (x,y coordinates for each body part). Standard approaches:
- Temporal CNN or transformer over keypoint sequences
- Graph neural networks over the pose skeleton
- Contrastive pretraining on unlabeled mouse behavior

Unusual domain for a generalist ML practitioner — Cameron likely entered for the learning value or competition prize size rather than domain expertise.

⚠️ *Stub — rank, score, and approach not confirmed from API data.*

## Related competitions

**Motion/behavior cluster:** [[wiki/kaggle/motion-s-text-to-sign.md]] is the inverse problem — generating motion from text rather than classifying behavior from motion. Both operate on temporal skeletal sequences. [[wiki/kaggle/jaguar-re-identification.md]] also uses visual sequences for identity/behavior tasks.
