---
title: "ADR: Open Model (Llama 3.3 70B) vs. Frontier Model for Trading Sentiment"
type: decision
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [wiki/trading/autotrader.md, wiki/trading/rsi-llm-signal-strategy.md, wiki/models/llama.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [adr, trading, llm, cost, open-source, llama, inference]
---

# ADR: Open Model (Llama 3.3 70B) vs. Frontier Model for Trading Sentiment

## Decision

Use Llama 3.3 70B via HuggingFace Inference API for news sentiment analysis rather than a frontier model (GPT-4o, Claude Sonnet).

## Context

AutoTrader scans top 50 stocks every 15 minutes during market hours (~6.5 hours/day). Each scan calls the LLM once per candidate ticker after RSI filtering. Even with RSI pre-filtering, this generates a high volume of LLM calls daily.

Market hours: ~390 minutes. Scan interval: 15 min. Scans/day: ~26.
If 20 tickers pass RSI filter per scan: **~520 LLM calls/day**.

## Cost comparison (approximate, 2026 rates)

| Model | Input cost / 1M tokens | ~520 calls/day cost | Monthly |
|-------|----------------------|---------------------|---------|
| GPT-4o | ~$2.50 | ~$1.30/day | ~$39 |
| Claude Sonnet | ~$3.00 | ~$1.56/day | ~$47 |
| **Llama 3.3 70B (HF API)** | **~$0.23** | **~$0.12/day** | **~$3.60** |

At paper trading scale, frontier model costs are manageable. But the goal is to eventually scale to live trading with tighter cost controls. Establishing the open model pattern now avoids a costly refactor later.

## Decision rationale

1. **Cost at scan frequency** — ~10× cheaper than frontier models for this use case
2. **Task complexity** — news sentiment classification is well within the capability of a 70B model; does not require frontier reasoning
3. **HF Inference API** — no infrastructure to manage; same API pattern as frontier models
4. **Future-proofing** — open model pattern is correct for high-frequency, lower-stakes LLM calls; frontier models reserved for high-stakes single-shot analysis

## Tradeoffs accepted

- **Quality ceiling** — Llama 3.3 70B may miss nuanced sentiment signals that GPT-4o would catch (e.g., subtle short-squeeze setups, regulatory language)
- **Inference latency** — HF Inference API can be slower than direct OpenAI/Anthropic endpoints under load
- **Less reliable JSON output** — open models sometimes produce malformed structured outputs; requires robust parsing + fallback handling

## General principle encoded

**Use open models for high-frequency, lower-stakes reasoning. Reserve frontier models for high-stakes, low-frequency analysis.**

This applies beyond trading: document classification pipelines, batch data enrichment, routing decisions — all are candidates for open model inference. Reserve GPT-4o / Claude Sonnet for: customer-facing responses, complex multi-step reasoning, ambiguous edge cases.

## Interview framing

"I made a deliberate cost architecture decision in AutoTrader: Llama 3.3 70B via HF Inference API for high-frequency sentiment calls, instead of GPT-4o. At 520 LLM calls/day the cost difference is 10×. The task — headline sentiment classification — is well within a 70B model's capability. I think about model selection the same way I think about compute tiers: match the model capability to the task complexity, don't over-provision."
