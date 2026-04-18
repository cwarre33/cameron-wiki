---
title: Cameron's Kaggle Portfolio — Overview
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: [[wiki/kaggle/deep-past-akkadian-translation.md]], [[wiki/kaggle/motion-s-text-to-sign.md]], [[wiki/kaggle/arc-agi-benchmarking.md]], [[wiki/kaggle/arc-prize-2025.md]], [[wiki/kaggle/stanford-rna-3d-folding.md]], [[wiki/kaggle/urban-flood-modelling.md]], [[wiki/kaggle/hull-tactical-market-prediction.md]], [[wiki/kaggle/aimo-progress-prize-3.md]], [[wiki/kaggle/march-machine-learning-mania-2026.md]], [[wiki/kaggle/playground-s6e2-heart-disease.md]], [[wiki/kaggle/csiro-image2biomass.md]], [[wiki/kaggle/jaguar-re-identification.md]], [[wiki/kaggle/mabe-mouse-behavior.md]], [[wiki/kaggle/google-tunix-hackathon.md]], [[wiki/kaggle/house-prices-regression.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [kaggle, portfolio, overview, competition]
---

# Cameron's Kaggle Portfolio — Overview

**14 competitions entered** across NLP, bioinformatics, CV, mathematical reasoning, quantitative finance, sports analytics, and wildlife ID. Total prize pool across entered competitions: ~$3.8M.

## Pattern

Cameron enters high-value, technically demanding competitions across diverse domains — generalist ML practitioner applying engineering patterns (MBR decoding, retrieval, pseudo-labeling, ensembling) to new problem spaces. Consistently reaches for the right tool for each domain rather than a single stack.

## Confirmed Results

| Competition | Rank | Score | Top Score | Method |
|---|---|---|---|---|
| [[wiki/kaggle/motion-s-text-to-sign.md\|Motion-S Text-to-Sign]] | **25** (active) | 0.43263 | 0.44241 | TF-IDF + kNN retrieval |
| [[wiki/kaggle/urban-flood-modelling.md\|Urban Flood Modelling]] | 117 | 0.5304 | 0.0120 | flood-model-v2 |
| [[wiki/kaggle/house-prices-regression.md\|House Prices Regression]] | ~19 | 0.00044 RMSLE | 0.00000 | TensorFlow Decision Forests |
| [[wiki/kaggle/deep-past-akkadian-translation.md\|Deep Past (Akkadian)]] | outside top 200 (legit) | 34.7 | 42.9 | [[wiki/models/byt5.md\|ByT5]] + [[wiki/techniques/mbr-decoding.md\|MBR]] |
| [[wiki/kaggle/deep-past-akkadian-translation.md\|Deep Past — leakage]] | ~1st / top 1% | — | — | Found + documented data leakage |

## All Competitions

### Closed

| Competition | Prize | Deadline | Page |
|---|---|---|---|
| Deep Past — Akkadian Translation | $50,000 | 2026-03-23 | [[wiki/kaggle/deep-past-akkadian-translation.md]] |
| Stanford RNA 3D Folding Part 2 | $75,000 | 2026-03-25 | [[wiki/kaggle/stanford-rna-3d-folding.md]] |
| AI Mathematical Olympiad Progress Prize 3 | $2,207,152 | 2026-04-15 | [[wiki/kaggle/aimo-progress-prize-3.md]] |
| March Machine Learning Mania 2026 | $50,000 | 2026-04-07 | [[wiki/kaggle/march-machine-learning-mania-2026.md]] |
| UrbanFloodBench | $7,000 | 2026-03-15 | [[wiki/kaggle/urban-flood-modelling.md]] |
| Jaguar Re-Identification | Kudos | 2026-03-14 | [[wiki/kaggle/jaguar-re-identification.md]] |
| Predicting Heart Disease (PGS6E2) | Swag | 2026-02-28 | [[wiki/kaggle/playground-s6e2-heart-disease.md]] |
| CSIRO Image2Biomass | $75,000 | 2026-01-28 | [[wiki/kaggle/csiro-image2biomass.md]] |
| Google Tunix Hackathon | $100,000 | 2026-01-12 | [[wiki/kaggle/google-tunix-hackathon.md]] |
| MABe Mouse Behavior Detection | $50,000 | 2025-12-15 | [[wiki/kaggle/mabe-mouse-behavior.md]] |
| ARC Prize 2025 | $1,000,000 | 2025-11-03 | [[wiki/kaggle/arc-prize-2025.md]] |
| House Prices (perpetual) | Knowledge | 2030-01-01 | [[wiki/kaggle/house-prices-regression.md]] |

### Active

| Competition | Prize | Deadline | Page |
|---|---|---|---|
| Motion-S Text-to-Sign | Kudos | 2026-05-10 | [[wiki/kaggle/motion-s-text-to-sign.md]] |
| Hull Tactical Market Prediction | $100,000 | 2026-06-16 | [[wiki/kaggle/hull-tactical-market-prediction.md]] |

## Supporting Infrastructure

Cameron also built [[wiki/kaggle/arc-agi-benchmarking.md]] — a production-grade async multi-provider LLM test harness for ARC-AGI tasks. Not a competition entry itself, but the tooling behind the ARC Prize 2025 entry.

## Domain Coverage

| Domain | Competitions |
|---|---|
| NLP / Translation | Deep Past, Google Tunix |
| Mathematical Reasoning | AIMO |
| Bioinformatics | Stanford RNA, CSIRO Biomass |
| Computer Vision | Jaguar Re-ID, CSIRO Biomass |
| Environmental ML | Urban Flood |
| Sign Language / Motion | Motion-S, MABe |
| Quantitative Finance | Hull Tactical |
| Sports Analytics | March Mania |
| Tabular ML | Heart Disease, House Prices |
| Reasoning Benchmarks | ARC Prize |

## Techniques Used Across Competitions

- [[wiki/techniques/mbr-decoding.md]] — Deep Past
- [[wiki/models/byt5.md]] — Deep Past
- TF-IDF + kNN retrieval — Motion-S
- RealMLP + CatBoost + XGBoost + SHAP — Heart Disease
- Pseudo-labeling — Stanford RNA
- Multi-GPU embeddings — Stanford RNA
- TFDF — House Prices
- LLM inference loops — ARC Prize 2025
