---
title: Stanford RNA 3D Folding (Part 2)
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/kaggle/deep-past-akkadian-translation.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, bioinformatics, rna, 3d-folding, structural-biology, pseudo-labeling]
---

# Stanford RNA 3D Folding (Part 2)

**Competition:** Stanford RNA 3D Folding Part 2
**Prize:** $75,000 | **Deadline:** 2026-03-25 (closed)
**Cameron's rank:** Unknown

## What it is

Predict the 3D structure of RNA molecules from sequence alone. RNA folding is a fundamental unsolved problem in structural biology — the RNA equivalent of AlphaFold for proteins. Accurate structure prediction enables drug design and understanding of gene regulation.

## Cameron's notebooks

- `stanford-rna-3d-folding-top-1-solution` — Study/reproduction of the top-1 solution
- `separated-embeddings-multigpu` — Multi-GPU embedding separation experiment
- `separated-embeddings-notebook` — Single-GPU version
- `pseudo-labeling` — Semi-supervised technique using model predictions as labels

## Techniques explored

**Pseudo-labeling** — use a model trained on labeled data to generate soft labels for unlabeled sequences, then train on both real + pseudo-labeled data. Effective when labeled data is scarce (which it is in structural biology).

**Separated embeddings (multi-GPU)** — suggests Cameron was working with large embedding models and needed to partition them across GPUs, likely for inference on a memory-constrained Kaggle environment.

⚠️ *Cameron's actual rank and approach are not confirmed from API data. This page is inferred from notebook titles. Update when results are available.*

## Domain notes

RNA structure prediction requires understanding:
- Primary sequence → secondary structure (base pairing)
- Secondary structure → tertiary 3D structure
- Existing tools: RoseTTAFold2NA, AlphaFold3 (limited RNA), EternaFold

This is a significantly harder domain than NLP — Cameron was entering as a generalist ML practitioner applying engineering patterns (pseudo-labeling, multi-GPU inference) to a bioinformatics problem.
