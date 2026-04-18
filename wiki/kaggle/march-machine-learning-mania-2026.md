---
title: March Machine Learning Mania 2026
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: []
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, sports-analytics, basketball, march-madness, bracket-prediction]
---

# March Machine Learning Mania 2026

**Competition:** March Machine Learning Mania 2026
**Prize:** $50,000 | **Deadline:** 2026-04-07 (closed)
**Cameron's rank:** Outside top 200 | **Top score:** 0.1097454 (log loss, lower is better)

## What it is

Predict NCAA March Madness tournament outcomes. Each submission is a probability distribution over all possible game outcomes for the tournament bracket. Scored by log loss — calibration matters as much as accuracy.

## Cameron's approach

Notebook `[44/50] LET ME (over)COOK!!!` — the 44/50 framing suggests Cameron was tracking something at a game/round level, possibly bracket accuracy. The "[LET ME COOK]" title implies he was optimizing aggressively.

Typical approaches for this competition:
- Seed-based baselines (strong and hard to beat)
- Elo / team strength ratings (KenPom, NET rankings)
- Historical upset rates by round + seed differential
- Ensemble of power ratings

⚠️ *Cameron's actual methodology is unconfirmed from API data. This is a stub.*

## Context

March Mania is notoriously hard to beat simple seed-based baselines on. The top of the leaderboard (log loss ~0.11) represents near-optimal calibration. Most ML approaches overfit to historical patterns that don't generalize to a specific year's bracket.
