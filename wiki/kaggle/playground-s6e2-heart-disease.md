---
title: Predicting Heart Disease (Playground S6E2)
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: []
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, tabular, classification, health, xgboost, neural-network, shap]
---

# Predicting Heart Disease — Playground Series S6E2

**Competition:** Predicting Heart Disease (Playground Series Season 6, Episode 2)
**Prize:** Swag | **Deadline:** 2026-02-28 (closed)
**Cameron's rank:** Outside top 200 | **Top score:** 0.95535 (AUC, higher is better)

## What it is

Binary classification: predict whether a patient has heart disease from clinical features (age, cholesterol, ECG results, etc.). Standard tabular ML competition on a synthetic dataset generated from real heart disease data.

## Cameron's notebooks

Three iterations showing a methodical approach:

1. `still-naive-2-0` — early/baseline approach
2. `s6e2-nn` — neural network attempt
3. `realmlp-cat-xgb-shap-analysis` — **RealMLP + CatBoost + XGBoost ensemble with SHAP analysis**

## Approach highlights

**RealMLP** — a "realistic" MLP architecture designed to be competitive with gradient boosting on tabular data (vs. vanilla MLP which usually loses to XGB).

**Ensemble: RealMLP + CatBoost + XGBoost** — standard winning recipe for Kaggle tabular competitions. Each model captures different signal; average probabilities reduce variance.

**SHAP analysis** — SHapley Additive exPlanations for feature importance and model interpretability. Shows which features drive predictions. Useful both for improving the model and for competition forums.

## What Cameron learned

The notebook progression shows the classic tabular Kaggle workflow:
- Start naive → identify what's not working
- Try a NN (often doesn't beat boosting on tabular)
- Move to gradient boosting ensemble + interpretability layer

⚠️ *Final rank and score not confirmed. Stub.*
