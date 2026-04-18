---
title: Llama 3.3 70B
type: model
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [[wiki/trading/autotrader.md]], [[wiki/tools/groq.md]], [[wiki/decisions/autotrader-open-model-vs-frontier.md]], [[wiki/models/clip.md]], [[wiki/models/byt5.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [model, llm, llama, meta, open-source, instruction-following, sentiment]
---

# Llama 3.3 70B

Meta's open-weights instruction-tuned LLM. Released late 2024. **70B parameters** — large enough for strong reasoning and instruction following, small enough to run cost-effectively on hosted inference APIs like [[wiki/tools/groq.md\|Groq]].

## Why this model

Cameron chose Llama 3.3 70B for [[wiki/trading/autotrader.md]] because:

1. **Cost** — ~10× cheaper than GPT-4o at the same token volume. At 50 stocks × every 15 minutes, cost per call is a real constraint.
2. **Sufficient capability** — sentiment classification from news headlines is a well-structured task. It doesn't require frontier-level reasoning, just reliable JSON output and calibrated bullish/bearish/neutral classification.
3. **Speed via Groq** — runs on Groq LPUs with very low latency, which matters for the 15-minute scan loop.
4. **Open weights** — no vendor lock-in; could self-host if needed.

See [[wiki/decisions/autotrader-open-model-vs-frontier.md]] for the full ADR.

## Key capabilities

- Strong instruction following and structured output (JSON)
- Multilingual (though Cameron uses English only)
- 128K context window
- Competitive with GPT-3.5-turbo class on most benchmarks
- Available via Groq, Together AI, Replicate, Ollama (local)

## Limitations for this use case

- No real-time market data access (Cameron supplies this via Alpaca News API)
- Occasional hallucinated news headlines — mitigated by passing actual headlines in the prompt
- Not as strong as GPT-4o/Claude 3.5 on complex multi-step reasoning tasks

## Prompt pattern used in AutoTrader

```
Analyze the following news for [TICKER].
Return JSON: {"sentiment": "bullish"|"bearish"|"neutral", "confidence": 0.0-1.0, "reasoning": "..."}

News: [headlines from Alpaca News API]
```

## Model family context

| Model | Params | Use case |
|-------|--------|---------|
| Llama 3.2 1B/3B | Small | On-device, edge inference |
| Llama 3.1 8B | Medium | Fast inference, simple tasks |
| **Llama 3.3 70B** | Large | **Cameron's choice — balanced cost/quality** |
| Llama 3.1 405B | XL | Research, complex reasoning |
