---
title: AI Mathematical Olympiad — Progress Prize 3
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/benchmarks/arc-agi.md]], [[wiki/kaggle/arc-prize-2025.md]], [[wiki/kaggle/google-tunix-hackathon.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, math, reasoning, olympiad, llm, aimo]
---

# AI Mathematical Olympiad — Progress Prize 3

**Competition:** AI Mathematical Olympiad - Progress Prize 3
**Prize:** $2,207,152 | **Deadline:** 2026-04-15 (just closed)
**Cameron's rank:** Outside top 200 | **Top score:** 45/50

## What it is

Solve International Mathematical Olympiad (IMO)-style problems automatically. Problems require multi-step symbolic reasoning, proof construction, and mathematical creativity. The $2.2M prize is for advancing toward AI systems that can compete at the IMO level.

## Scoring

The metric appears to be number of problems solved correctly (top score: 45). The practice-set notebook `[44/50] LET ME (over)COOK!!!` suggests Cameron was tracking problem-level accuracy during development — 44 out of 50 on an evaluation set.

⚠️ *It's unclear whether the 44/50 notebook refers to this competition or March Machine Learning Mania (basketball bracket scoring). Given the notebook title style, it may be March Mania. The AIMO correlation is speculative.*

## Context

AIMO is one of the hardest active ML competitions. Top teams in 2024-2025 used:
- Extended chain-of-thought (o1-style reasoning)
- Symbolic math engines (Lean, Mathematica) as verifiers
- Self-play and MCTS for proof search

Cameron entering this competition reflects ambition; it's a frontier research problem, not an applied ML task.

## Cameron's approach

Unknown — rank outside top 200, no distinctive notebook titles confirmed for AIMO. May have used frontier LLM prompting with chain-of-thought.

⚠️ *This is a stub. Update with actual approach and final rank when available.*

## Related competitions

**Reasoning cluster:** [[wiki/kaggle/arc-prize-2025.md]] is the other anti-memorization reasoning competition Cameron entered — visual abstract reasoning vs. mathematical reasoning. Both test whether models can genuinely generalize rather than pattern-match training data (see [[wiki/benchmarks/arc-agi.md]]). [[wiki/kaggle/google-tunix-hackathon.md]] overlaps on the "show your work" / chain-of-thought dimension.
