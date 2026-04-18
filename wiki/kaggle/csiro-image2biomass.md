---
title: CSIRO — Image2Biomass Prediction
type: kaggle-competition
status: active
visibility: public
sources: [raw/kaggle/cameron-kaggle-profile.md]
related: []
created: 2026-04-17
updated: 2026-04-17
confidence: low
tags: [kaggle, computer-vision, biomass, remote-sensing, regression, environmental-ml]
---

# CSIRO — Image2Biomass Prediction

**Competition:** CSIRO - Image2Biomass Prediction
**Prize:** $75,000 | **Deadline:** 2026-01-28 (closed)
**Cameron's rank:** Outside top 200 | **Top score:** 0.67899

## What it is

Predict above-ground biomass from satellite or drone imagery. CSIRO (Australian scientific research agency) competition on remote sensing regression — map image pixels to biomass density estimates.

## Cameron's approach

Notebook `csiro_biomass_baseline_english` — Cameron created a starter/baseline notebook, possibly a public resource for other competitors (common in Kaggle: publish a clean baseline to gain upvotes and visibility).

## Domain context

Image-to-biomass is a regression problem over satellite imagery. Typical approaches:
- CNN backbone (ResNet, EfficientNet) pretrained on ImageNet
- Geospatial augmentation (random crop/flip of satellite tiles)
- Multi-spectral fusion if NIR/SWIR bands available
- Post-processing with spatial smoothing

⚠️ *Stub — rank, score, and detailed approach not confirmed from API data.*
