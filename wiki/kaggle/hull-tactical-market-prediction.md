---
title: Hull Tactical — Market Prediction
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/trading/autotrader.md]], [[wiki/trading/rsi-llm-signal-strategy.md]], [[wiki/integrations/alpaca-api.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, trading, market-prediction, quantitative-finance, active]
---

# Hull Tactical — Market Prediction

**Competition:** Hull Tactical - Market Prediction
**Prize:** $100,000 | **Deadline:** 2026-06-16 (ACTIVE)
**Cameron's rank:** Unknown — competition still running

## What it is

Predict market movements for Hull Tactical Asset Management, a quantitative hedge fund. Likely involves predicting short-term returns, volatility, or direction for financial instruments.

## Cameron's connection

Directly overlaps with Cameron's AutoTrader work — [[wiki/trading/autotrader.md]] uses RSI + LLM sentiment signals for paper trading. Hull Tactical likely requires:
- Time-series feature engineering (returns, volatility, momentum)
- Cross-asset signal construction
- Walk-forward validation (no look-ahead leakage)

Cameron's notebooks include `[LB 0.0] Time and Chance Happen to Them All` — the "[LB 0.0]" prefix is a Kaggle convention for notebooks that submit a constant prediction to establish a leaderboard baseline. This is a methodical starting point.

## Notable notebooks

- `lb-0-0-time-and-chance-happen-to-them-all` — constant-prediction baseline
- `lb-0-0-time-and-chance-happen-to-them-all-16b69e` — variant

⚠️ *Active competition. Rank and approach unknown. Update as Cameron progresses.*

## Domain context

Hull Tactical's research focuses on tactical asset allocation — rotating between risk-on and risk-off based on macro signals. The competition likely rewards:
- Factor-based features (momentum, mean-reversion, macro)
- Regime detection (bull/bear/sideways)
- Robust out-of-sample validation

Connects to Cameron's [[wiki/trading/rsi-llm-signal-strategy.md]] — RSI is a momentum factor.
