---
title: Groq — LLM Inference API
type: tool
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [[wiki/trading/autotrader.md]], [[wiki/architectures/agentic-trading-system.md]], [[wiki/decisions/autotrader-open-model-vs-frontier.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [tool, inference, groq, llm, api, latency, open-source-models]
---

# Groq — LLM Inference API

Groq provides ultra-low-latency inference for open-source LLMs via custom LPU (Language Processing Unit) hardware. Primary value proposition: **significantly faster token generation than GPU-based inference**, at lower cost than frontier APIs.

## Why Cameron uses it

AutoTrader scans 50 stocks every 15 minutes, requiring an LLM sentiment call per stock per scan. At that frequency, latency and cost per call are the binding constraints — not raw model quality.

Groq's speed + Llama 3.3 70B's sufficient capability = the right tradeoff. See [[wiki/decisions/autotrader-open-model-vs-frontier.md]].

## Key properties

- **Latency:** Token generation measured in hundreds of tokens/second vs. ~30–60 tokens/second on typical GPU inference
- **Models available:** Llama 3.x (8B, 70B), Mixtral, Gemma, others — open-source weights only
- **API compatibility:** OpenAI-compatible chat completions endpoint — drop-in for many applications
- **Pricing:** Token-based, cheaper than GPT-4o/Claude for equivalent open-source models

## Usage in Cameron's stack

```python
from groq import Groq
client = Groq(api_key=os.environ["GROQ_API_KEY"])
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)
```

## Tradeoffs

| Factor | Groq + Llama 70B | OpenAI GPT-4o |
|--------|-----------------|---------------|
| Latency | Very low | Moderate |
| Cost | ~10× cheaper | Baseline |
| Capability | Strong for structured tasks | Stronger for nuanced reasoning |
| Data privacy | Groq servers | OpenAI servers |

## Where used

- [[wiki/trading/autotrader.md]] — 15-minute stock sentiment analysis loop
- [[wiki/architectures/agentic-trading-system.md]] — the deployment architecture
