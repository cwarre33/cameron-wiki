---
title: Hull Tactical — Market Prediction
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md, raw/kaggle/hull-tactical-base-gateway.py, raw/kaggle/hull-tactical-relay.py, raw/kaggle/hull-tactical-data-schema.txt]
related: [[wiki/trading/autotrader.md]], [[wiki/trading/rsi-llm-signal-strategy.md]], [[wiki/integrations/alpaca-api.md]], [[wiki/decisions/hull-tactical-strategy.md]], [[wiki/benchmarks/arc-agi.md]]
created: 2026-04-17
updated: 2026-04-18
confidence: high
tags: [kaggle, trading, market-prediction, quantitative-finance, grpc, interactive-api, active]
---

# Hull Tactical — Market Prediction

**Competition:** Hull Tactical - Market Prediction
**Prize:** $100,000 | **Deadline:** 2026-06-16 (ACTIVE)
**Cameron's rank:** Baseline established; strategy in development

## What it is

Predict market movements (forward returns) for Hull Tactical Asset Management — a quantitative hedge fund focused on tactical asset allocation. The competition uses Kaggle's **interactive time-series evaluation API** (gRPC-based), not static CSV submission. Predictions are made incrementally, one day at a time, with lagged outcomes revealed as the evaluation progresses.

## Data schema

Pulled directly via Kaggle API (2026-04-18). Train: 9,049 rows (daily), 98 columns.

| Group | Count | Interpretation |
|-------|-------|----------------|
| D1–D9 | 9 binary (0/1) | Discrete regime/threshold signals (RSI-style triggers) |
| E1–E20 | 20 continuous | Equity/sector factors |
| I1–I9 | 9 continuous | Index/market factors |
| M1–M18 | 18 continuous | Macro/momentum factors |
| S1–S12 | 12 continuous | Sentiment/spread factors |
| V1–V13 | 13 continuous | Volatility/volume factors |
| P1–P13 | 13 continuous | Price/premium factors |

**Targets:** `forward_returns`, `risk_free_rate`, `market_forward_excess_returns`

**Test set** additionally provides: `lagged_forward_returns`, `lagged_risk_free_rate`, `lagged_market_forward_excess_returns` — the previous day's revealed outcomes, enabling online learning.

Early training rows (date_id 0–~200) have NaN for all continuous features — only D features are available during the warm-up period.

## Evaluation API (gRPC — interactive, not static)

The model runs as a gRPC server. The Kaggle evaluation gateway calls it day by day:

```
for each day in test window:
    gateway sends: all feature columns for date_id N
    your model must return: predicted forward_return for date_id N
    gateway reveals: lagged outcome from date_id N-1
```

Key files in `raw/kaggle/`:
- `hull-tactical-base-gateway.py` — `BaseGateway` loop: `generate_data_batches()` → `predict()` → `write_submission()`
- `hull-tactical-relay.py` — gRPC relay, port 50051, 5-retry policy, unlimited message size

**This is walk-forward evaluation by design.** The API enforces temporal ordering — you cannot look ahead.

## AutoTrader connection

**Critical insight:** Hull Tactical's D features (binary 0/1) are structurally identical to what AutoTrader computes at runtime:

| AutoTrader component | Hull Tactical equivalent |
|---------------------|--------------------------|
| RSI threshold (overbought/oversold = 1/0) | D1–D9 (binary regime flags) |
| LLM news sentiment score | E/S features (continuous contextual factors) |
| Dual-gate: both must align | Combine D signals + E/S features in model |
| 15-min scan loop | Day-by-day gRPC evaluation |
| `decisions.jsonl` + outcomes | Lagged outcomes in test features |

AutoTrader *computes* signals from raw market data. Hull Tactical *provides* pre-computed, anonymized signals. The signal logic is the same — the implementation layer is different.

See [[wiki/decisions/hull-tactical-strategy.md]] for the full approach ADR.

## Notable notebooks

- `lb-0-0-time-and-chance-happen-to-them-all` — constant-prediction baseline (LB 0.0)
- `lb-0-0-time-and-chance-happen-to-them-all-16b69e` — variant

## Domain context

Hull Tactical's research focuses on tactical asset allocation — rotating between risk-on and risk-off based on macro signals. This competition rewards:
- **Binary signal interpretation** — D features as directional triggers (momentum, mean reversion thresholds)
- **Continuous factor combination** — E/M/S/V as regime context
- **Walk-forward discipline** — enforced by the gRPC API
- **Online adaptation** — lagged outcomes are revealed, enabling Bayesian/incremental model updates

Connects to [[wiki/trading/rsi-llm-signal-strategy.md]] — RSI is a momentum factor; the D-group are likely pre-computed versions of signals like RSI crossovers, moving average crossovers, volatility thresholds.
