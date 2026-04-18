"""
Hull Tactical — Market Prediction
Kaggle Submission Notebook

Strategy: D + M features (27 total), LightGBM, walk-forward trained.
IC baseline: +0.043 (std=0.010) on 5-fold walk-forward CV.

Model: LightGBM regressor trained on full train.csv
Features: D1-D9 (binary regime flags) + M1-M18 (macro/momentum factors)
Target: forward_returns

To submit:
1. Upload hull_dm_model.txt as a Kaggle dataset
2. Paste this notebook into a Kaggle notebook
3. Point MODEL_PATH to your dataset path
4. Run as "Submit to Competition"

Local test:
    python hull-tactical-submission.py
    (Uses train.csv split for offline validation)
"""

import json
import numpy as np
import pandas as pd
import lightgbm as lgb
import kaggle_evaluation.core.relay as relay

# ── Config ──────────────────────────────────────────────────────────────────

MODEL_PATH = '/kaggle/input/hull-tactical-model/hull_dm_model.txt'

# Median imputation values from train.csv (embedded to avoid train data leakage)
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

# ── Model loading ────────────────────────────────────────────────────────────

model = lgb.Booster(model_file=MODEL_PATH)

# Running sum of lagged returns for online signal enrichment
_recent_outcomes = []
_MAX_RECENT = 20

# ── Prediction function ──────────────────────────────────────────────────────

def predict(features: pd.DataFrame) -> float:
    """
    Called once per day by the Kaggle evaluation gateway.

    features: DataFrame with one row — all competition feature columns plus
              lagged_forward_returns, lagged_risk_free_rate,
              lagged_market_forward_excess_returns on test days.

    Returns: float — predicted forward_return for this day.
    """
    # Extract D + M features, fill any NaN with train medians
    row = features[FEATURE_COLS].fillna(MEDIANS_SERIES)

    # Append lagged outcome signal if available
    if 'lagged_forward_returns' in features.columns:
        lag = features['lagged_forward_returns'].iloc[0]
        if pd.notna(lag):
            _recent_outcomes.append(lag)
            if len(_recent_outcomes) > _MAX_RECENT:
                _recent_outcomes.pop(0)

    pred = float(model.predict(row)[0])

    # Attenuate prediction if recent outcomes strongly contradict the signal
    # (simple online confidence adjustment — scales prediction toward zero when
    # recent realized returns disagree with recent predictions)
    if len(_recent_outcomes) >= 5:
        recent_mean = np.mean(_recent_outcomes[-5:])
        if np.sign(recent_mean) != np.sign(pred) and abs(recent_mean) > 0.003:
            pred *= 0.5  # half-confidence when recent regime contradicts

    return pred


# ── gRPC server ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # On Kaggle: gateway calls predict() via gRPC. Start the server and block.
    server = relay.define_server(predict)
    server.start()
    server.wait_for_termination()
