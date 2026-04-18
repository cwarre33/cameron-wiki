"""
Hull Tactical — Market Prediction
Kaggle Submission Notebook

Strategy: D + M features (27 total), LightGBM, walk-forward trained.
IC baseline: +0.043 (std=0.010) on 5-fold walk-forward CV.

Model: LightGBM regressor trained on full train.csv
Features: D1-D9 (binary regime flags) + M1-M18 (macro/momentum factors)
Target: forward_returns

To submit: see review/SETUP.md
"""

import json
import pathlib
import numpy as np
import pandas as pd
import lightgbm as lgb
import kaggle_evaluation.core.relay as relay

# ── Config ───────────────────────────────────────────────────────────────────

MODEL_PATH = '/kaggle/input/hull-tactical-model/hull_dm_model.txt'
LOG_PATH = pathlib.Path('/kaggle/working/predictions.jsonl')

MEDIANS = {
    "D1": 0.0, "D2": 0.0, "D3": 0.0, "D4": 1.0, "D5": 0.0,
    "D6": 0.0, "D7": 0.0, "D8": 0.0, "D9": 0.0,
    "M1": -0.8092533771, "M2": -0.020768034,  "M3": -0.14435585,
    "M4":  0.054151155,  "M5":  0.4074538797, "M6": -0.1383237314,
    "M7": -0.0425176755, "M8":  0.4227843915, "M9": -0.10088449999,
    "M10": 0.119819037,  "M11":-0.28509798705,"M12": 0.4835745,
    "M13":-1.09183350645,"M14":-0.79136265,   "M15": 0.4933862434,
    "M16": 0.0006613757, "M17": 0.22371031745,"M18": 0.7007275132,
}

FEATURE_COLS = sorted(MEDIANS.keys())
MEDIANS_SERIES = pd.Series(MEDIANS)

# ── Model + state ─────────────────────────────────────────────────────────────

model = lgb.Booster(model_file=MODEL_PATH)
_recent_outcomes: list[float] = []
_MAX_RECENT = 20

# ── Prediction function ───────────────────────────────────────────────────────

def predict(features: pd.DataFrame) -> float:
    row = features[FEATURE_COLS].fillna(MEDIANS_SERIES)

    lag = None
    if 'lagged_forward_returns' in features.columns:
        raw_lag = features['lagged_forward_returns'].iloc[0]
        if pd.notna(raw_lag):
            lag = float(raw_lag)
            _recent_outcomes.append(lag)
            if len(_recent_outcomes) > _MAX_RECENT:
                _recent_outcomes.pop(0)

    pred = float(model.predict(row)[0])
    attenuated = False

    if len(_recent_outcomes) >= 5:
        recent_mean = np.mean(_recent_outcomes[-5:])
        if np.sign(recent_mean) != np.sign(pred) and abs(recent_mean) > 0.003:
            pred *= 0.5
            attenuated = True

    # Write structured log for weekly LLM review
    log_entry = {
        'date_id': int(features['date_id'].iloc[0]),
        'D': {c: int(row[c].iloc[0]) for c in FEATURE_COLS if c.startswith('D')},
        'M_top4': {c: round(float(row[c].iloc[0]), 4) for c in ['M4', 'M3', 'M1', 'M8']},
        'pred': round(pred, 6),
        'lagged_return': round(lag, 6) if lag is not None else None,
        'attenuated': attenuated,
    }
    with LOG_PATH.open('a') as f:
        f.write(json.dumps(log_entry) + '\n')

    return pred


# ── gRPC server ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    server = relay.define_server(predict)
    server.start()
    server.wait_for_termination()
