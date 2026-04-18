---
title: Hull Tactical — Competition Lab
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/hull-tactical-base-gateway.py, raw/kaggle/hull-tactical-relay.py, raw/kaggle/hull-tactical-data-schema.txt]
related: [[wiki/kaggle/hull-tactical-market-prediction.md]], [[wiki/decisions/hull-tactical-strategy.md]], [[wiki/trading/autotrader.md]], [[wiki/trading/rsi-llm-signal-strategy.md]]
created: 2026-04-18
updated: 2026-04-18
confidence: high
tags: [kaggle, lab, hull-tactical, active, lightgbm, grpc, walk-forward]
---

# Hull Tactical — Competition Lab

Active implementation log for the Hull Tactical - Market Prediction competition ($100k, deadline 2026-06-16).

**Strategy:** [[wiki/decisions/hull-tactical-strategy.md]] — AutoTrader dual-gate signal architecture mapped to anonymized features. LightGBM + walk-forward CV + gRPC server.

---

## Implementation phases

### Phase 1 — Walk-forward baseline (target: week 1–2)
- [ ] Load `train.csv`, handle NaN warm-up period (date_id 0–~200, only D features valid)
- [ ] Build `TimeSeriesSplit` walk-forward harness (5 folds, expanding window)
- [ ] Train `LGBMRegressor` on D1–D9 + full feature set, target = `forward_returns`
- [ ] Score: information coefficient (rank correlation) + excess return over `market_forward_excess_returns`
- [ ] Establish local IC baseline before any submission

### Phase 2 — Feature group ablation (target: week 2–3)
- [ ] D only → IC score (binary gate value in isolation)
- [ ] D + E → does equity context add signal?
- [ ] D + M → macro/momentum factors
- [ ] D + S → sentiment/spread
- [ ] Full feature set → does adding everything help or overfit?
- [ ] Feature importance plot: which D flags and continuous features actually drive predictions?
- [ ] Check: is the model actually beating market benchmark or just predicting noise?

### Phase 3 — gRPC server (target: week 3–4)
- [ ] Implement `predict()` endpoint using `BaseGateway` from `raw/kaggle/hull-tactical-base-gateway.py`
- [ ] Handle `lagged_forward_returns` as an online feature (yesterday's outcome feeds today's prediction)
- [ ] Test locally using `data_paths` argument for offline iteration
- [ ] Package model + server as Kaggle notebook submission

```python
import kaggle_evaluation.core.base_gateway as bg
import lightgbm as lgb

class HullGateway(bg.BaseGateway):
    def __init__(self):
        super().__init__(target_column_name='forward_returns')
        self.model = lgb.Booster(model_file='model.txt')

    def predict(self, features_df):
        return self.model.predict(features_df)[0]
```

### Phase 4 — LLM review loop (target: week 4+)
- [ ] Build prediction history log: `{date_id, features_summary, prediction, lagged_outcome}`
- [ ] Weekly LLM pass: which D-flag regimes are currently predictive? Which are failing?
- [ ] Use summaries to inform feature subset selection or model recalibration
- [ ] Mirrors AutoTrader's `daily_review.jsonl` → [[wiki/techniques/llm-review-pass-before-rotation.md]]

---

## Experiment log

| Date | Phase | What was tried | IC result | Notes |
|------|-------|---------------|-----------|-------|
| — | — | — | — | Baseline not yet run |

---

## Key constraints

- **Deadline:** 2026-06-16
- **Evaluation:** gRPC interactive API — walk-forward, no look-ahead
- **Early rows:** date_id 0–~200 have NaN for all continuous features; impute or mask
- **Benchmark to beat:** `market_forward_excess_returns` column (not zero)
- **Do not use:** future feature values, any look-ahead imputation across train/test boundary
