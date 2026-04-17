---
title: ARC-AGI Benchmark
type: benchmark
status: active
visibility: public
sources: [raw/repos/arc-agi-benchmarking-readme.md]
related: [[wiki/kaggle/arc-agi-benchmarking.md]], [[wiki/comparisons/llm-wiki-vs-rag.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [benchmark, arc-agi, reasoning, abstraction, few-shot, francois-chollet]
---

# ARC-AGI Benchmark

**Abstraction and Reasoning Corpus for Artificial General Intelligence.** Created by François Chollet. The benchmark that specifically resists LLM memorization — every task is a novel visual reasoning puzzle.

## What it tests

ARC-AGI presents small grid-based visual transformation tasks. Given a few (input → output) demonstration pairs, the model must infer the transformation rule and apply it to a new input. **No task appears in training data by design.**

This makes it one of the few benchmarks where memorization genuinely cannot explain high performance. A model that solves ARC-AGI tasks must generalize the rule from first principles.

## Why it matters

Most LLM benchmarks (MMLU, HumanEval) are vulnerable to data contamination — models can achieve high scores by having seen similar problems during training. **ARC-AGI is specifically designed to prevent this.** It's a measure of sample-efficient, abstract reasoning — closer to what Chollet calls "true intelligence."

## Versions

| Version | Notes |
|---------|-------|
| ARC-AGI-1 | Original 2019 corpus; frontier models now score ~75–85% |
| ARC-AGI-2 | Harder variant (2024/2025); current frontier models score much lower. Core benchmark for [[wiki/kaggle/arc-prize-2025.md]]. |

Same task format for both — swap `--data_dir` in Cameron's harness.

## Cameron's connection

Cameron built [[wiki/kaggle/arc-agi-benchmarking.md]] to run frontier models directly against both versions. Rather than citing published leaderboard numbers, he can measure models himself — and compare cost vs. accuracy across providers.

## Key claim

**ARC-AGI score is a more honest signal of reasoning capability than most benchmarks.** ⚠️ This is contested — some researchers argue the visual-grid format is its own learnable skill. But the anti-contamination design is genuine.
