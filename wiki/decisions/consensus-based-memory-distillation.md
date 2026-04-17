---
title: "ADR: Consensus-Based Memory Distillation"
type: decision
status: proposed
visibility: public
related: [[wiki/techniques/mbr-decoding.md]], [[wiki/techniques/llm-review-pass-before-rotation.md]], [[wiki/decisions/arc-agi-adapters-vs-litellm.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [adr, architecture, memory, mbr, consensus, agentic-drift]
---

# ADR: Consensus-Based Memory Distillation

## Context

Current agentic systems (e.g., [[wiki/trading/autotrader.md|AutoTrader]]) rely on a single-pass [[wiki/techniques/llm-review-pass-before-rotation.md|LLM Review Pass]] to distill logs into long-term lessons. This is vulnerable to "Agentic Drift"—where a single model hallucination or biased interpretation is permanently committed to the knowledge base, potentially leading to cascading failures in future decision cycles.

Conversely, our work in [[wiki/kaggle/deep-past-akkadian-translation.md|Deep Past]] successfully used [[wiki/techniques/mbr-decoding.md|Minimum Bayes Risk (MBR) Decoding]] to find consensus among multiple noisy translation candidates.

## Decision

We will implement **Consensus-Based Memory Distillation**. Instead of a single-pass review, the system will:
1. Generate $N$ independent distillation candidates (lessons/summaries) for a given batch of logs.
2. Apply a semantic similarity-based MBR selection to identify the "Consensus Summary."
3. Reject summaries with a high "Disagreement Score" (variance), flagging them for human review rather than automatic commit.

## Rationale

- **Anti-Hallucination**: By requiring multiple generations to agree on a "lesson," we filter out one-off model hallucinations.
- **Provider Agnostic**: Using the [[wiki/architectures/provider-adapter-pattern.md|Provider Adapter Pattern]], we can cross-examine models (e.g., GPT-4o vs. Claude 3.5) to find the "Median Truth."
- **Quantifiable Confidence**: The divergence between candidates provides a mathematical metric for "Memory Confidence," allowing the bot to reduce position sizes when its understanding of the market regime is "noisy."
- **Semantic Density**: The resulting lessons are "cleaner" and more stable, improving the signal-to-noise ratio for long-horizon context windows.

## Consequences

- **Increased Token Cost**: Moving from $1$ pass to $N$ passes ($N \approx 5-10$) increases inference costs. This necessitates using cheaper "open" models (e.g., Llama 3.3 70B via Groq) for the generation phase.
- **Latency**: Distillation becomes a batch-process rather than a real-time one, though this fits the existing 24-hour rotation cycle.
- **Stable Intelligence**: The agent's "World Model" becomes more resistant to sudden regime shifts and more reliable over months of autonomous operation.

## Related

- [[wiki/techniques/mbr-decoding.md]] — The mathematical foundation.
- [[wiki/techniques/llm-review-pass-before-rotation.md]] — The original single-pass implementation.
- [[wiki/open-questions/agentic-memory-retention-strategies.md]] — The broader strategic context.
