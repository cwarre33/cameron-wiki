---
title: ARC-AGI Benchmarking Harness
type: kaggle-competition
status: active
visibility: public
sources: [raw/repos/arc-agi-benchmarking-readme.md]
related: [[wiki/benchmarks/arc-agi.md]], [[wiki/architectures/provider-adapter-pattern.md]], [[wiki/decisions/arc-agi-adapters-vs-litellm.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [arc-agi, benchmarking, llm-evaluation, async, multi-provider, python]
---

# ARC-AGI Benchmarking Harness

**Cameron's fork of [arcprizeorg/model_baseline](https://github.com/arcprizeorg/model_baseline).** A production-grade async test harness for running frontier LLMs against ARC-AGI-1 and ARC-AGI-2 reasoning tasks.

## What it does

Runs a configurable set of models against ARC-AGI tasks and scores their outputs against ground truth. Supports multiple providers (OpenAI, Anthropic, Google, Grok) via a clean adapter interface. Results are submittable to HuggingFace.

## Architecture

```
cli/run_all.py          — async batch runner; all (task × model) pairs run concurrently
main.py                 — single-task debug runner
src/.../adapters/       — one adapter per provider, all implement ProviderAdapter
src/arc_agi_benchmarking/models.yml      — model registry with pricing
provider_config.yml     — per-provider rate limits
src/scoring/scoring.py  — ground-truth validation
```

The batch runner pairs every task with every model config and fans them out via `asyncio`. See [[wiki/architectures/provider-adapter-pattern.md]] for the adapter design.

## Key engineering decisions

- **Custom adapters over LiteLLM** — see [[wiki/decisions/arc-agi-adapters-vs-litellm.md]]
- **Per-provider rate limiting** — Anthropic allows 1000 req/60s, Gemini only 60; limits are config-driven, not hardcoded
- **`tenacity` exponential backoff** — transient API errors are retried automatically without crashing a long run
- **Multiple attempts per task** — `--num_attempts` (default: 2) lets you run each task twice and take the best, reducing variance
- **Cost tracking at model level** — `models.yml` stores `input`/`output` price per 1M tokens; enables price/accuracy analysis across models

## models.yml schema

```yaml
models:
  - name: "config_name"
    model_name: "actual-model-id"
    provider: "openai|anthropic|gemini"
    max_tokens: 4024
    temperature: 0.0
    pricing:
      date: "YYYY-MM-DD"
      input: 0.00    # per 1M tokens
      output: 0.00
```

## Rate limits observed (2026)

| Provider | Requests/60s |
|----------|-------------|
| OpenAI   | 5,000       |
| Anthropic | 1,000      |
| Gemini   | 60          |

## Key CLI flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--task_list_file` | — | .txt of task IDs to run |
| `--model_configs` | — | comma-separated config names from models.yml |
| `--num_attempts` | 2 | attempts per task |
| `--retry_attempts` | 2 | retries on API failure |
| `--enable-metrics` | off | collect timing data |
| `--overwrite_submission` | off | overwrite existing results |
| `--data_dir` | — | path to ARC-AGI-1 or ARC-AGI-2 data |

## Why ARC-AGI matters

ARC-AGI measures abstract reasoning that **cannot be solved by pattern-matching training data** — each task is a novel visual puzzle. Strong ARC-AGI scores are a genuine signal of reasoning capability, not memorization. Cameron built this harness to measure frontier models directly rather than citing published leaderboard numbers. See [[wiki/benchmarks/arc-agi.md]].

## Portfolio angle

- Demonstrates understanding of async concurrency, rate limiting, and retry patterns at the infrastructure layer
- Cost-aware evaluation design (pricing in model config) shows production engineering instincts
- Provider abstraction via strategy pattern shows software design maturity
- Directly comparable to work done by AI labs' evals teams
