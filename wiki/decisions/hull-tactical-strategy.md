---
title: "ADR: Hull Tactical Strategy — AutoTrader Signal Stack as Feature Pipeline"
type: decision
status: active
visibility: public
sources: [raw/kaggle/hull-tactical-base-gateway.py, raw/kaggle/hull-tactical-relay.py, raw/kaggle/hull-tactical-data-schema.txt, raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/kaggle/hull-tactical-market-prediction.md]], [[wiki/trading/autotrader.md]], [[wiki/trading/rsi-llm-signal-strategy.md]], [[wiki/decisions/autotrader-open-model-vs-frontier.md]], [[wiki/decisions/autotrader-decisions-log-retention.md]], [[wiki/techniques/llm-review-pass-before-rotation.md]]
created: 2026-04-18
updated: 2026-04-18
confidence: medium
tags: [adr, kaggle, trading, hull-tactical, grpc, walk-forward, feature-engineering, autotrader]
---

# ADR: Hull Tactical Strategy — AutoTrader Signal Stack as Feature Pipeline

## Decision

**Treat the AutoTrader dual-gate signal architecture as the conceptual frame for interpreting Hull Tactical's anonymized features, then train a gradient-boosted model with walk-forward cross-validation.**

Specifically:
- D1–D9 (binary) → treated as pre-computed momentum/regime triggers (AutoTrader's RSI gate)
- E/M/S/V features (continuous) → treated as contextual/sentiment factors (AutoTrader's LLM gate)
- gRPC interface → walk-forward evaluation loop; mirror this in local validation
- Lagged outcomes → use as online features or for Bayesian weight adjustment between days

## Context

Hull Tactical provides 9,049 days of training data with 94 anonymized features across 7 groups (D, E, I, M, P, S, V) plus 3 target columns. The evaluation is gRPC-based: predictions are made one day at a time via an interactive API, with the previous day's actual return revealed as each new batch arrives.

Key discovery (2026-04-18 via Kaggle API): **D features are binary (0/1) in both training and test data.** This is structurally identical to RSI threshold signals in AutoTrader — a binary "regime gate." The continuous features (E, M, S, V, P, I) play the role of contextual modifiers that determine whether a detected regime should be acted on.

## Rationale

### Why this frame?

Cameron already built a system that combines binary momentum signals with continuous contextual signals (AutoTrader). The Hull Tactical feature structure maps cleanly onto this:

```
AutoTrader:
  RSI < 30 (binary: oversold = 1)  ×  LLM sentiment > threshold → BUY
  
Hull Tactical:
  D5 = 1 (binary regime flag)  ×  S3, M7, E12 (continuous context) → predict positive forward_return
```

The mapping is conceptual, not literal — we don't know what D5 means. But the **combination structure** is the same: binary gates that say "regime is active" + continuous features that say "how strong/reliable."

### Why gradient boosting over LLM-based approach?

- Features are fully anonymized — LLM news sentiment cannot help (no tickers, no text)
- The signal structure is tabular — GBDT (LightGBM/XGBoost) is the benchmark approach for this
- D features being binary makes tree splits natural and efficient
- LLM involvement is reserved for feature interpretation / strategy adaptation in the review loop (see below)

### Why walk-forward, not random split?

The gRPC evaluation API enforces temporal ordering. **Any model trained with random CV will overfit to regime patterns that don't generalize to the test window.** Walk-forward (expanding or sliding window) mirrors how the evaluation actually works.

⚠️ Early rows (date_id 0–~200) have NaN for all continuous features — only D features are valid. Imputation or feature masking is required for these rows.

## Implementation plan

### Phase 1 — Local walk-forward baseline (weeks 1–2)

```python
# Walk-forward skeleton
from sklearn.model_selection import TimeSeriesSplit
import lightgbm as lgb

tscv = TimeSeriesSplit(n_splits=5)
for fold_idx, (train_idx, val_idx) in enumerate(tscv.split(X)):
    model = lgb.LGBMRegressor(...)
    model.fit(X.iloc[train_idx], y.iloc[train_idx])
    preds = model.predict(X.iloc[val_idx])
    # Score: information coefficient (rank correlation) with forward_returns
    # Also: excess over market_forward_excess_returns (the real benchmark)
```

**Target:** `forward_returns` (regression). Primary metric: IC (rank correlation). Secondary: Sharpe-equivalent of predictions used as allocation weights.

### Phase 2 — Feature groups ablation (week 2–3)

Systematically test which feature groups matter:
- D only (binary gates) — establishes baseline regime signal value
- D + E (add equity context) — how much do equity factors help?
- D + M (add macro) — momentum factors
- Full feature set — does adding everything help or hurt?

This mirrors AutoTrader's question: "does LLM sentiment add signal over RSI alone?"

### Phase 3 — gRPC server implementation (week 3–4)

```python
import kaggle_evaluation.core.base_gateway as bg

class HullTacticalGateway(bg.BaseGateway):
    def __init__(self):
        super().__init__(target_column_name='forward_returns')
        self.model = lgb.Booster(model_file='model.txt')
        self.feature_history = []
    
    def predict(self, features_df):
        # features_df is one row: all D, E, I, M, P, S, V columns
        # plus lagged_forward_returns (yesterday's actual outcome)
        pred = self.model.predict(features_df)
        return pred[0]
```

The `lagged_forward_returns` column in test is a key advantage — it reveals whether yesterday's trade worked. This enables **online adaptation**: adjust confidence weights based on recent prediction accuracy.

### Phase 4 — LLM-driven strategy review loop (week 4+)

Borrow directly from [[wiki/techniques/llm-review-pass-before-rotation.md]]:

- Every 7 days, run a review pass over the prediction history (feature state → prediction → revealed outcome)
- LLM summarizes: which feature regimes are currently predictive? Which are failing?
- Use summaries to inform model recalibration or feature subset selection
- This is the Hull Tactical equivalent of AutoTrader's `daily_review.jsonl`

## Feature engineering hypotheses

| Feature group | AutoTrader analogue | Hypothesis |
|--------------|--------------------|----|
| D1–D9 (binary) | RSI overbought/oversold | Momentum crossover signals; D4=1 may mean "price above 200d MA" |
| E1–E20 | LLM equity sentiment | Sector rotation signals; cross-sectional equity factors |
| M1–M18 | N/A (AutoTrader has no macro) | Macro regime: VIX, yield curve, credit spreads (anonymized) |
| S1–S12 | Partially: news sentiment | Sentiment/spread; credit spread may be here |
| V1–V13 | Partially: news volatility | Realized vs. implied vol; VIX term structure |
| I1–I9 | N/A | Index momentum factors |
| P1–P13 | N/A | Premium factors: value, carry, quality |

⚠️ These are hypotheses. The anonymization means we cannot verify. Feature importance from GBDT training will inform which groups actually matter.

## What carries over from AutoTrader

| AutoTrader component | Hull Tactical application |
|---------------------|--------------------------|
| Dual-gate architecture | Binary D + continuous E/M/S/V combination |
| 90-day decisions log rotation | Sliding-window training (recency bias is correct in markets) |
| LLM review pass before rotation | Weekly strategy review on prediction history |
| Outcome log (indefinite) | Full prediction+outcome JSONL → long-run IC tracking |
| Confidence threshold | Only trade (predict non-zero weight) when D signal is unambiguous |

## What must be built

1. **Imputation strategy** for NaN-heavy early rows — median imputation per group is safest baseline
2. **gRPC server** implementing `predict()` endpoint (see Phase 3 above)
3. **Walk-forward validation harness** with IC as primary metric
4. **Online feature tracker** that ingests `lagged_forward_returns` as a running feature
5. **Local offline test mode** — `BaseGateway` supports this via `data_paths` argument; use `train.csv` split for local iteration before Kaggle submission

## Risks

- **Feature group misidentification** — our interpretations of D/E/M/S/V are speculative. Start with data-driven feature importance, not assumptions.
- **Regime change during test window** — the test window starts at date_id=8980. If market regime shifted after training data ends, all regime-specific signals are stale. Need structural break detection.
- **gRPC timeout** — relay.py sets a 5-retry policy but your `predict()` must be fast. LightGBM inference is <1ms per row; acceptable.
- **90-day sliding window may be wrong** — it's right for AutoTrader (regime changes frequently). For Hull Tactical, the optimal lookback is empirical — test expanding vs. sliding window in ablation.

## Related decisions

- [[wiki/decisions/autotrader-decisions-log-retention.md]] — retain-outcomes/rotate-reasoning principle applies here
- [[wiki/decisions/autotrader-open-model-vs-frontier.md]] — why Llama 3.3 was chosen for AutoTrader; for Hull Tactical, no LLM is in the prediction path (features are anonymized), but LLM fits in the review loop
