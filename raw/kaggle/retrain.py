"""
Hull Tactical — retrain model on full train.csv.
Run locally after weekly review recommends changes.

Usage:
    python retrain.py                          # default: D+M, 300 trees
    python retrain.py --drop D4               # drop a noisy D flag
    python retrain.py --drop D4 D7 --trees 400
    python retrain.py --features D M S        # change feature groups

Output: model_files/hull_dm_model.txt (ready to upload as Kaggle dataset)
"""

import argparse
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.model_selection import TimeSeriesSplit

TRAIN_PATH = '/tmp/hull_train.csv'
OUTPUT_DIR = Path('model_files')
OUTPUT_DIR.mkdir(exist_ok=True)

ALL_GROUPS = ['D', 'E', 'I', 'M', 'P', 'S', 'V']

MEDIANS_PATH = Path('/tmp/hull_dm_medians.json')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--features', nargs='+', default=['D', 'M'],
                   choices=ALL_GROUPS, help='feature groups to include')
    p.add_argument('--drop', nargs='*', default=[], help='specific columns to drop (e.g. D4 D7)')
    p.add_argument('--trees', type=int, default=300)
    p.add_argument('--lr', type=float, default=0.04)
    p.add_argument('--leaves', type=int, default=31)
    p.add_argument('--min-child', type=int, default=50)
    return p.parse_args()


def main():
    args = parse_args()

    df = pd.read_csv(TRAIN_PATH)
    all_feature_cols = [c for c in df.columns
                        if c not in ['date_id', 'forward_returns', 'risk_free_rate',
                                     'market_forward_excess_returns']]

    feature_cols = [c for c in all_feature_cols
                    if c[0] in args.features and c not in args.drop]

    print(f"Features: {len(feature_cols)} cols from groups {args.features}, dropped: {args.drop or 'none'}")

    medians = df[feature_cols].median()
    X = df[feature_cols].fillna(medians)
    y = df['forward_returns']

    # Walk-forward validation
    tscv = TimeSeriesSplit(n_splits=5)
    ics = []
    for train_idx, val_idx in tscv.split(X):
        m = lgb.LGBMRegressor(
            n_estimators=args.trees, learning_rate=args.lr,
            num_leaves=args.leaves, min_child_samples=args.min_child,
            subsample=0.8, colsample_bytree=0.8, random_state=42, verbose=-1
        )
        m.fit(X.iloc[train_idx], y.iloc[train_idx])
        preds = m.predict(X.iloc[val_idx])
        ic, _ = spearmanr(preds, y.iloc[val_idx])
        ics.append(ic)

    print(f"Walk-forward IC: mean={np.mean(ics):+.4f}  std={np.std(ics):.4f}  folds={ics}")

    # Train on full dataset
    model = lgb.LGBMRegressor(
        n_estimators=args.trees, learning_rate=args.lr,
        num_leaves=args.leaves, min_child_samples=args.min_child,
        subsample=0.8, colsample_bytree=0.8, random_state=42, verbose=-1
    )
    model.fit(X, y)

    model_path = OUTPUT_DIR / 'hull_dm_model.txt'
    model.booster_.save_model(str(model_path))
    medians.to_json(OUTPUT_DIR / 'hull_dm_medians.json')

    print(f"Saved: {model_path}")
    print(f"Saved: {OUTPUT_DIR / 'hull_dm_medians.json'}")
    print(f"\nNext: kaggle datasets version -p {OUTPUT_DIR} -m 'retrain {np.mean(ics):+.4f} IC'")


if __name__ == '__main__':
    main()
