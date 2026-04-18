# Graph Report - .  (2026-04-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 123 nodes · 144 edges · 32 communities detected
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]

## God Nodes (most connected - your core abstractions)
1. `wiki/index.md — Master Catalog` - 14 edges
2. `Agentic Trading System Architecture` - 13 edges
3. `ADR: Consensus-Based Memory Distillation` - 10 edges
4. `LLM Review Pass Before Rotation` - 8 edges
5. `wiki/overview.md — High-Level Synthesis` - 8 edges
6. `wiki/log.md — Append-Only Activity Log` - 8 edges
7. `ARC-AGI Benchmarking Harness` - 7 edges
8. `ADR: Wiki Retention Policy` - 7 edges
9. `Jaguar Re-Identification Challenge` - 7 edges
10. `Cameron Kaggle Profile (raw source)` - 7 edges

## Surprising Connections (you probably didn't know these)
- `LLM Wiki Pattern (Karpathy)` --semantically_similar_to--> `Graphify — Knowledge Graph Skill`  [INFERRED] [semantically similar]
  wiki/methodology/llm-wiki-pattern.md → CLAUDE.md
- `ARC-AGI Benchmarking Harness` --references--> `ARC-AGI Benchmarking README (raw)`  [EXTRACTED]
  wiki/kaggle/arc-agi-benchmarking.md → raw/repos/arc-agi-benchmarking-readme.md
- `ARC-AGI Benchmarking Harness` --semantically_similar_to--> `Agentic Trading System Architecture`  [INFERRED] [semantically similar]
  wiki/kaggle/arc-agi-benchmarking.md → wiki/architectures/agentic-trading-system.md
- `Cost Tracking at Model Level` --semantically_similar_to--> `ADR: Open Model vs. Frontier for Trading Sentiment`  [INFERRED] [semantically similar]
  wiki/kaggle/arc-agi-benchmarking.md → wiki/decisions/autotrader-open-model-vs-frontier.md
- `Agentic Trading System Architecture` --references--> `AutoTrader README (raw)`  [EXTRACTED]
  wiki/architectures/agentic-trading-system.md → raw/repos/autotrader-readme.md

## Hyperedges (group relationships)
- **Consensus-Based Memory Distillation: MBR + LLM Review + Provider Adapters applied to agentic memory** — doc_consensus_memory_adr, concept_mbr_decoding, concept_llm_review_pass, concept_provider_adapter_pattern, concept_autotrader, concept_agentic_memory_retention [EXTRACTED 0.95]
- **LLM Wiki System: index + log + overview form the maintenance backbone of the wiki** — doc_index, doc_log, doc_overview, concept_llm_wiki_pattern, doc_claudemd [EXTRACTED 0.92]
- **Frontier reasoning benchmarks: AIMO + ARC-AGI + chain-of-thought as shared frontier ML challenge space** — doc_aimo_prize_3, concept_arc_agi, concept_chain_of_thought, concept_aimo_math_reasoning [INFERRED 0.75]
- **Tabular ML Kaggle competitions cluster — House Prices and Heart Disease both use gradient boosting on structured data** — kaggle_house_prices_regression, kaggle_playground_s6e2_heart_disease, technique_xgboost, technique_gradient_boosting_ensemble, concept_tabular_ml [INFERRED 0.85]
- **Computer vision wildlife competitions cluster — Jaguar Re-ID and MABe both involve animal visual recognition with embedding/contrastive methods** — kaggle_jaguar_reidentification, kaggle_mabe_mouse_behavior, technique_metric_learning, technique_clip_faiss, concept_computer_vision_kaggle [INFERRED 0.75]
- **LLM reasoning research cluster — Google Tunix, chain-of-thought, and process reward models form a coherent research direction** — kaggle_google_tunix_hackathon, technique_chain_of_thought [INFERRED 0.78]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.2
Nodes (21): ADR: 90-Day Rotating Retention for Trading Decisions Log, Agentic Drift (hallucination compounding in memory), Open Question — Agentic Memory Retention Strategies, Mathematical Olympiad / IMO-level Reasoning, ARC-AGI Benchmark, ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI, AutoTrader — Autonomous Paper Trading Bot, Chain-of-Thought Reasoning (o1-style) (+13 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (17): Agentic Trading System Architecture, HuggingFace Spaces Docker Deployment, Health Check as First-Class Concern, JSONL Persistent Feedback Loop, Self-Improvement Loop Design, Single Entrypoint + Shared Lib Pattern, ADR: 90-Day Rotating Retention for Decisions Log, ADR: Open Model vs. Frontier for Trading Sentiment (+9 more)

### Community 2 - "Community 2"
Cohesion: 0.2
Nodes (14): Computer Vision (Kaggle competitions), Log Loss / Calibration (March Mania), CSIRO — Image2Biomass Prediction, Google Tunix Hackathon, Jaguar Re-Identification Challenge, MABe — Social Action Recognition in Mice, March Machine Learning Mania 2026, SofaScope Production System (+6 more)

### Community 3 - "Community 3"
Cohesion: 0.27
Nodes (12): Agentic Memory Compression via Distillation, AutoTrader Decisions-Log Retention (decisions.jsonl / outcomes.jsonl), MemGPT / Letta Tiered Memory, Quarterly Lint Pass (/lint workflow), Retain Outcomes / Rotate Reasoning Principle, Speculative Page Pruning (90-day staleness threshold), Weekly Review Pass (AutoTrader weekly_review.py), ADR: Wiki Retention Policy (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (7): Async Batch Runner (asyncio fan-out), Config-Driven Model Selection (models.yml), Cost Tracking at Model Level, Per-Provider Rate Limiting (config-driven), Tenacity Exponential Backoff, ARC-AGI Benchmarking Harness, ARC-AGI Benchmarking README (raw)

### Community 5 - "Community 5"
Cohesion: 0.38
Nodes (7): Tabular ML (Kaggle), House Prices — Advanced Regression Techniques, Predicting Heart Disease — Playground Series S6E2, Gradient Boosting Ensemble (XGBoost + CatBoost + RealMLP), SHAP (SHapley Additive exPlanations), TensorFlow Decision Forests (TFDF), XGBoost

### Community 6 - "Community 6"
Cohesion: 0.38
Nodes (7): Graphify — Knowledge Graph Skill, LLM Wiki Pattern (Karpathy), Obsidian Integration, Retrieval-Augmented Generation (RAG), CLAUDE.md — Wiki Schema & Workflows, Andrej Karpathy, Rationale: Compiling > Re-deriving (LLM Wiki vs RAG)

### Community 7 - "Community 7"
Cohesion: 0.5
Nodes (5): Deep Past: Akkadian Translation, Motion-S: Text-to-Sign Motion Generation, ByT5 (Byte-Level T5), LLM Review Pass Before Rotation, MBR Decoding (Minimum Bayes Risk)

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (4): Provider Adapter Pattern (Multi-LLM), ADR: Custom Provider Adapters vs. LiteLLM, Rationale for Custom Adapters, LiteLLM

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (3): cameron-wiki README, Wiki Index — Master Catalog, Activity Log — Append-Only Ingest History

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (3): Consensus-Based Memory Distillation, LLM Review Pass, MBR Decoding

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (3): SofaScope — AI-Powered Furniture Visual Search, CLIP + FAISS Visual Search Pipeline, Persistent Model Loading Pattern

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): FAISS Vector Search Tool

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): Abstract Reasoning (anti-memorization benchmark)

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): wiki/kaggle/arc-agi-benchmarking.md

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): LLM Wiki vs. RAG Comparison

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): The LLM Wiki Pattern

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Cameron's Wiki Setup

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): CLIP Model

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): ADR: Metadata Scoring vs. Embeddings for Text Search

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): ADR: Persistent Service stdin/stdout vs. HTTP

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): System Design — Visual Search at Scale

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Persistent Model Loading Pattern

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): SofaScope README (raw)

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Karpathy LLM Wiki Gist (raw)

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Cameron's Second Brain — Overview

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Agentic Trading System Architecture

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmark

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): ARC Prize 2025

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmarking Harness

## Knowledge Gaps
- **53 isolated node(s):** `FAISS Vector Search Tool`, `Config-Driven Model Selection (models.yml)`, `Tenacity Exponential Backoff`, `Abstract Reasoning (anti-memorization benchmark)`, `wiki/kaggle/arc-agi-benchmarking.md` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (1 nodes): `FAISS Vector Search Tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `Abstract Reasoning (anti-memorization benchmark)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `wiki/kaggle/arc-agi-benchmarking.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `LLM Wiki vs. RAG Comparison`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `The LLM Wiki Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `Cameron's Wiki Setup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `CLIP Model`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `ADR: Metadata Scoring vs. Embeddings for Text Search`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `ADR: Persistent Service stdin/stdout vs. HTTP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `System Design — Visual Search at Scale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Persistent Model Loading Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `SofaScope README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Karpathy LLM Wiki Gist (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Cameron's Second Brain — Overview`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Agentic Trading System Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `ARC-AGI Benchmark`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `ARC Prize 2025`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `ARC-AGI Benchmarking Harness`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Agentic Trading System Architecture` connect `Community 1` to `Community 4`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `wiki/index.md — Master Catalog` connect `Community 0` to `Community 6`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `Cameron Kaggle Profile (raw source)` connect `Community 2` to `Community 5`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `FAISS Vector Search Tool`, `Config-Driven Model Selection (models.yml)`, `Tenacity Exponential Backoff` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._