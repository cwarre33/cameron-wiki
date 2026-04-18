---
title: House Prices — Advanced Regression Techniques
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: []
created: 2026-04-17
updated: 2026-04-17
confidence: medium
tags: [kaggle, tabular, regression, house-prices, beginner, xgboost, tfdf]
---

# House Prices — Advanced Regression Techniques

**Competition:** House Prices - Advanced Regression Techniques
**Prize:** Knowledge (beginner/practice) | **Deadline:** 2030-01-01 (perpetual)
**Cameron's rank:** ~19 | **Score:** 0.00044 RMSLE | **Top score:** 0.00000 RMSLE

## What it is

The canonical Kaggle beginner competition. Predict Ames, Iowa house sale prices from 79 features. Uses RMSLE (Root Mean Squared Log Error) — lower is better.

## Cameron's result

RMSLE of 0.00044 is near-perfect. Rank ~19 in the top-200 shown by the leaderboard API.

**Important context:** House Prices is a perpetual competition with thousands of teams, many of which have submitted near-perfect scores over the years. The top of the leaderboard is heavily inflated by teams that have effectively reverse-engineered the test labels (the dataset is old and well-known). Cameron's 0.00044 is genuinely strong but should be read in that context.

## Cameron's approach

Notebook `house-prices-prediction-using-tfdf` — **TensorFlow Decision Forests (TFDF)**. Google's gradient-boosted tree library running in TF. An unusual choice vs. the standard XGBoost/LightGBM stack, suggesting Cameron was experimenting with the framework rather than optimizing for rank.

## Portfolio note

House Prices is a learning competition, not a competitive one. The value is in demonstrating tabular ML fundamentals: feature engineering (handling ordinal categoricals, log-transforming skewed targets), model selection, and validation strategy. Good for showing progression from beginner to practitioner.
