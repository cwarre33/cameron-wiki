---
title: AutoTrader — Autonomous Paper Trading Bot
type: trading-strategy
status: active
visibility: public
sources: [raw/repos/autotrader-readme.md]
related: [wiki/trading/rsi-llm-signal-strategy.md, wiki/decisions/autotrader-open-model-vs-frontier.md, wiki/decisions/autotrader-decisions-log-retention.md, wiki/integrations/alpaca-api.md, wiki/architectures/agentic-trading-system.md, wiki/models/llama.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [trading, alpaca, rsi, llm-sentiment, paper-trading, llama, gradio, docker, agentic]
---

# AutoTrader — Autonomous Paper Trading Bot

AI-powered paper trading bot. Scans top 50 most-active stocks every 15 minutes, applies RSI + LLM news sentiment as dual signal gates, and executes paper trades via Alpaca. **Paper trading only — no real capital.**

## Stack

- **LLM:** Llama 3.3 70B via HuggingFace Inference API
- **Broker:** Alpaca paper trading API
- **Technical analysis:** RSI (14-period, Wilder's smoothing)
- **News:** Alpaca News API (fetched per-ticker at scan time)
- **Dashboard:** Gradio UI — account summary, positions, trade history
- **Deployment:** Docker container, HF Spaces-compatible, 15-min cron scan
- **Alerts:** Discord bot integration

## Signal logic

Both signals must align to trigger a trade. Neither alone is sufficient.

```
RSI (momentum, backward-looking)
    +
LLM sentiment (news reaction, forward-looking)
    +
Confidence threshold
    ↓
Execute or skip
```

See [[wiki/trading/rsi-llm-signal-strategy.md]] for the strategy detail.

## Risk management

- **5% max position size** per trade — hard cap
- **Confidence threshold** — LLM must express sufficient certainty before execution
- **Paper only** — Alpaca paper trading account; no real capital at risk

## Architecture

```
cron (15min) → scan_autotrader.py
                    ↓
              lib/alpaca_client  → get top 50 by volume
                    ↓
              lib/rsi            → compute RSI per ticker
                    ↓
              Alpaca News API    → fetch headlines
                    ↓
              Llama 3.3 70B      → sentiment + reasoning
                    ↓
              lib/decisions      → log + execute/skip
                    ↓
              logs/outcomes.jsonl, decisions.jsonl, daily_review.jsonl
```

See [[wiki/architectures/agentic-trading-system.md]] for the full deployment pattern.

## Self-improvement loop

Every scan appends to persistent JSONL logs:

| File | Content | Retention |
|------|---------|-----------|
| `logs/outcomes.jsonl` | Per-trade P&L outcomes | Indefinite |
| `logs/decisions.jsonl` | Trade decisions + reasoning | 90 days (rotating) |
| `logs/daily_review.jsonl` | Daily summary | Indefinite |

This creates a feedback record for future analysis or LLM-driven strategy review. See [[wiki/decisions/autotrader-decisions-log-retention.md]].

## Key decisions

- **Why Llama 3.3 70B over GPT-4o?** Cost at scan frequency. See [[wiki/decisions/autotrader-open-model-vs-frontier.md]].
- **Why 90-day retention on decisions.jsonl?** Recency bias is intentional for trading — old market regimes shouldn't dominate current strategy.

## What would change for live trading

1. Swap Alpaca paper keys → live keys (surface change)
2. Full risk management audit (position sizing, drawdown limits, circuit breakers)
3. Latency review — 15-min scans are fine for swing-style; intraday would need faster scan loop
4. Cost model revisit — at live trading frequency, LLM inference costs become material

## Alpaca integration

See [[wiki/integrations/alpaca-api.md]] for API patterns, auth, and paper vs. live account handling.

## Related work

- [[wiki/trading/rsi-llm-signal-strategy.md]] — the dual-signal logic
- [[wiki/kaggle/hull-tactical-market-prediction.md]] — Cameron's active Kaggle entry in quant finance ($100k prize)
- [[wiki/integrations/alpaca-api.md]] — broker implementation detail
