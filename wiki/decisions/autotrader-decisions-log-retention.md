---
title: "ADR: 90-Day Rotating Retention for Trading Decisions Log"
type: decision
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [wiki/trading/autotrader.md, wiki/trading/rsi-llm-signal-strategy.md, wiki/open-questions/agentic-memory-retention-strategies.md, wiki/techniques/llm-review-pass-before-rotation.md, wiki/decisions/wiki-retention-policy.md]
created: 2026-04-17
updated: 2026-04-17
confidence: medium
tags: [adr, trading, memory, retention, agentic, feedback-loop]
---

# ADR: 90-Day Rotating Retention for Trading Decisions Log

## Decision

Rotate `logs/decisions.jsonl` on a 90-day window. Keep `logs/outcomes.jsonl` and `logs/daily_review.jsonl` indefinitely.

## Context

AutoTrader logs every trading decision (execute or skip, with LLM reasoning) to `decisions.jsonl`. This log serves two purposes:
1. **Audit trail** — understand why specific trades were made
2. **Self-improvement input** — feed back into the system for strategy review

As the log grows, older entries become less relevant to current market conditions. A rotating window prevents unbounded log growth and encodes a deliberate recency bias.

## Rationale

**Why 90 days for decisions, indefinite for outcomes?**

- `decisions.jsonl` captures *reasoning* — market context, sentiment signals, RSI values. These are regime-dependent. A decision made in a high-volatility regime (e.g., a market shock period) is a poor teacher for normal conditions 12 months later. 90 days captures roughly one market quarter — a natural regime boundary.

- `outcomes.jsonl` captures *results* — P&L per trade. These are useful indefinitely for long-run performance analysis, strategy comparison, and pattern detection across regimes.

- `daily_review.jsonl` captures *summaries* — lightweight enough to keep forever, and valuable for longitudinal performance review.

## The broader pattern: agentic memory with intentional forgetting

This is an instance of a general problem in agentic systems: **what should an agent remember vs. forget?**

| Memory type | Retention strategy | Rationale |
|------------|-------------------|-----------|
| Decisions (reasoning + context) | 90-day rotating | Regime-dependent; recency bias is correct |
| Outcomes (P&L results) | Indefinite | Regime-independent performance signal |
| Daily summaries | Indefinite | Low storage cost, high longitudinal value |

**General principle:** Retain outcomes indefinitely. Rotate reasoning context on a horizon that matches the domain's regime change frequency.

## Open questions

- ⚠️ 90 days is a heuristic, not derived from backtesting. Should be validated: does strategy quality degrade when trained on >90-day-old decisions?
- Could implement adaptive retention: keep decisions from high-performance periods longer, prune decisions from losing streaks faster.
- Future enhancement: LLM-driven weekly review pass over `decisions.jsonl` to extract durable lessons before rotation purges them.

## Related

- [[wiki/trading/autotrader.md]]
- [[wiki/open-questions/agentic-memory-retention-strategies.md]]
