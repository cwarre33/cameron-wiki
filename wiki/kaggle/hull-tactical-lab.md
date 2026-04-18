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

### Phase 1 — Walk-forward baseline ✅ (completed 2026-04-18)
- [x] Load `train.csv`, handle NaN warm-up (continuous features start at date_id ~1006, some as late as 6969)
- [x] Build `TimeSeriesSplit` walk-forward harness (5 folds, expanding window)
- [x] Train `LGBMRegressor` on all 94 features, target = `forward_returns`
- [x] Score: IC = **+0.028** (mean), 4/5 folds positive. Excess return/day = +0.000177.
- [x] Note: D6 is {-1, 0} not {0, 1} — short/neutral directional flag.

### Phase 2 — Feature group ablation ✅ (completed 2026-04-18)
- [x] D only → IC +0.010 (binary flags alone are weak)
- [x] D + E → IC +0.013 (equity adds little)
- [x] **D + M → IC +0.044** ← winner
- [x] D + S → IC +0.017
- [x] D + I → IC +0.005 (index factors useless)
- [x] D + V → IC −0.002 (volatility actively hurts — DROP)
- [x] D+E+M+S → IC +0.044 (equal to D+M; E and S add noise)
- [x] Full 94 → IC +0.028 (worse than D+M; P/V/I are noise)
- [x] **Decision: use D + M (27 features) as competition model**

### Phase 3 — gRPC server ✅ (completed 2026-04-18)
- [x] Submission script: `raw/kaggle/hull-tactical-submission.py`
- [x] Model: LightGBM, D+M (27 features), n_estimators=300, min_child_samples=50
- [x] Medians embedded directly (no train data leakage)
- [x] `lagged_forward_returns` used for online confidence adjustment: if recent 5-day mean return disagrees with prediction sign and |mean| > 0.3%, attenuate prediction by 50%
- [x] gRPC server: `relay.define_server(predict)` on port 50051

**To submit on Kaggle:**
1. Upload `hull_dm_model.txt` as a private Kaggle dataset named `hull-tactical-model`
2. Create a new notebook for the competition
3. Add dataset as input (`/kaggle/input/hull-tactical-model/`)
4. Paste `hull-tactical-submission.py` content as the notebook
5. Set notebook type to "Always On" (required for gRPC server pattern)
6. Submit to competition

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

### Phase 4 — LLM review loop ✅ (completed 2026-04-18)
- [x] Prediction log embedded in submission: writes `predictions.jsonl` to `/kaggle/working/` each day
- [x] Log schema: `{date_id, D flags dict, M_top4, pred, lagged_return, attenuated}`
- [x] `review/llm_review.py` — pulls log, computes IC proxy + D-flag regime breakdown, sends to Claude Sonnet, appends to `strategy_log.md`
- [x] `review/weekly_review.sh` — full weekly pipeline: `kaggle kernels output` → LLM review → leaderboard check → retrain prompt
- [x] `review/submit_notebook.py` — reusable Playwright automator for "Submit to Competition" button; saves session cookies to avoid weekly re-login
- [x] `retrain.py` — CLI for feature group changes: `--drop D4` removes a noisy flag, reruns walk-forward IC, saves model for dataset upload
- [x] `review/SETUP.md` — complete setup guide: dataset upload, notebook creation, session save, cron setup

**Weekly cadence:**
```
Sunday cron → weekly_review.sh
  → kaggle kernels output (pull predictions.jsonl)
  → llm_review.py (IC proxy + D-flag analysis + Claude recommendation)
  → if retrain needed: retrain.py --drop <flag> → dataset version → submit_notebook.py
```

---

## Experiment log

| Date | Phase | What was tried | IC result | Notes |
|------|-------|---------------|-----------|-------|
| 2026-04-18 | 1 | LightGBM, all 94 features, median impute, 5-fold walk-forward | +0.0283 (std 0.026) | 4/5 folds positive. Warm-up: continuous features don't start until date_id ~1006, some as late as 6969. D6 is {-1,0} not {0,1}. |
| 2026-04-18 | 2 | Feature ablation — D only | +0.0096 | Binary flags alone weak |
| 2026-04-18 | 2 | Feature ablation — D + E | +0.0125 | Equity factors barely help |
| 2026-04-18 | 2 | **Feature ablation — D + M** | **+0.0440** | **Best combo. Macro/momentum is the signal.** |
| 2026-04-18 | 2 | Feature ablation — D + S | +0.0173 | Sentiment/spread modest |
| 2026-04-18 | 2 | Feature ablation — D + I | +0.0045 | Index factors unhelpful |
| 2026-04-18 | 2 | Feature ablation — D + V | −0.0022 | Volatility features actively hurt |
| 2026-04-18 | 2 | Feature ablation — D+E+M+S | +0.0436 | Near-equal to D+M. E and S add noise over M alone. |
| 2026-04-18 | 2 | Feature ablation — Full (94) | +0.0283 | Worse than D+M. P/V/I add noise. |

### Key findings from ablation (2026-04-18)

- **D + M is the winning combo** (IC +0.044 vs +0.028 for full). Drop V, I, and reconsider P.
- **M features dominate importance**: M4, M3 are top-ranked. These are macro/momentum factors — the real predictive signal.
- **D features have conditional value**: D alone = IC +0.010 (weak), but D+M = +0.044. D flags tell the model *when* to trust the M signal, not what the signal is.
- **P features are deceptive**: Rank 4–12 in feature importance (P4, P3, P13, P6, P7, P5, P12) but including P with D hurts (not tested alone, but full > D+M). Likely capturing M's signal with extra noise.
- **AutoTrader analogy refined**: M ≈ "LLM sentiment" (continuous regime context), D ≈ RSI threshold gate. V/I = noise to drop.

### Next model: D + M only (27 features)

Submit D+M as the competition model. Use D+E+M+S as fallback if D+M overfits on test.

---

## Key constraints

- **Deadline:** 2026-06-16
- **Evaluation:** gRPC interactive API — walk-forward, no look-ahead
- **Early rows:** date_id 0–~200 have NaN for all continuous features; impute or mask
- **Benchmark to beat:** `market_forward_excess_returns` column (not zero)
- **Do not use:** future feature values, any look-ahead imputation across train/test boundary
