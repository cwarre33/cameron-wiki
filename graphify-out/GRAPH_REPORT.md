# Graph Report - .  (2026-07-29)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 113 nodes · 129 edges · 35 communities (8 shown, 27 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cbf49878`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Cameron's Kaggle Portfolio Overview — 14 Competitions
- Llama 3.3 70B — Meta Open-Weights LLM
- Groq — LLM Inference API
- Graphify Graph Report
- ADR: Consensus-Based Memory Distillation
- Wiki Index — Master Catalog
- CLAUDE.md — Wiki Schema & Workflows
- Jaguar Re-Identification Challenge
- CLIP + FAISS Visual Search Pipeline
- LiteLLM
- FAISS Vector Search Tool
- ARC Prize 2025
- Hull Tactical — Market Prediction
- ARC-AGI Benchmarking Harness
- Retrieval-Augmented Generation (RAG)
- Cameron's Wiki Setup
- Agentic Trading System Architecture
- CLIP — Contrastive Language-Image Pretraining
- ByT5 (Byte-Level T5)
- ADR: Wiki Retention Policy — Archive vs. Prune Speculative Pages
- ADR: Metadata Scoring vs. Embeddings for Text Search
- ADR: Persistent Service stdin/stdout vs. HTTP
- ADR: 90-Day Rotating Retention for Trading Decisions Log
- ADR: Open Model vs. Frontier for Trading Sentiment
- Alpaca API Integration
- System Design — Visual Search at Scale
- SofaScope — AI-Powered Furniture Visual Search
- ARC-AGI Benchmark
- Andrej Karpathy
- RSI + LLM Signal Strategy
- Hybrid Search Routing (Text + Image)
- AutoTrader README (raw)
- ARC-AGI Benchmarking README (raw)
- SofaScope README (raw)
- Karpathy LLM Wiki Gist (raw)

## God Nodes (most connected - your core abstractions)
1. `Wiki Index — Master Catalog` - 19 edges
2. `Cameron's Kaggle Portfolio Overview — 14 Competitions` - 12 edges
3. `Ingest: Cameron's Kaggle Profile — 14 Competitions` - 11 edges
4. `ADR: Consensus-Based Memory Distillation` - 9 edges
5. `Stanford RNA 3D Folding (Part 2)` - 9 edges
6. `Graphify Graph Report` - 9 edges
7. `Groq — LLM Inference API` - 8 edges
8. `Llama 3.3 70B — Meta Open-Weights LLM` - 7 edges
9. `Motion-S: Text-to-Sign Motion Generation (Rank 25)` - 7 edges
10. `CSIRO — Image2Biomass Prediction` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Graphify — Knowledge Graph Skill` --semantically_similar_to--> `LLM Wiki Pattern (Karpathy)`  [INFERRED] [semantically similar]
  CLAUDE.md → wiki/methodology/llm-wiki-pattern.md
- `SofaScope Visual Search System` --semantically_similar_to--> `CSIRO — Image2Biomass Prediction`  [INFERRED] [semantically similar]
  wiki/overview.md → wiki/kaggle/csiro-image2biomass.md
- `README — cameron-wiki` --references--> `CLAUDE.md — Wiki Schema & Workflows`  [EXTRACTED]
  README.md → CLAUDE.md
- `CLAUDE.md — Wiki Schema & Workflows` --references--> `LLM Wiki Pattern (Karpathy)`  [EXTRACTED]
  CLAUDE.md → wiki/methodology/llm-wiki-pattern.md
- `Jaguar Re-Identification Challenge` --references--> `Cameron Kaggle Profile (raw source)`  [EXTRACTED]
  wiki/kaggle/jaguar-re-identification.md → raw/kaggle/cameron-kaggle-profile.md

## Hyperedges (group relationships)
- **LLM Wiki System: index + log + overview form the maintenance backbone of the wiki** — concept_llm_wiki_pattern, doc_claudemd [EXTRACTED 0.92]
- **Computer vision wildlife competitions cluster — Jaguar Re-ID and MABe both involve animal visual recognition with embedding/contrastive methods** — kaggle_jaguar_reidentification, technique_metric_learning, technique_clip_faiss [INFERRED 0.75]
- **Consensus-Based Memory Distillation: MBR + LLM Review + Provider Adapters applied to agentic memory** — doc_consensus_memory_adr, concept_mbr_decoding, concept_llm_review_pass, concept_provider_adapter_pattern, concept_autotrader, concept_agentic_memory_retention [EXTRACTED 0.95]
- **Scientific/Environmental ML Kaggle Cluster — Stanford RNA, Urban Flood, CSIRO Biomass** — kaggle_stanford_rna, kaggle_urban_flood, kaggle_csiro, technique_pseudo_labeling, concept_rna_folding, concept_flood_geospatial, concept_biomass_prediction [EXTRACTED 0.88]
- **Tabular ML Kaggle Cluster — House Prices + Heart Disease + March Mania use gradient boosting on structured data** — kaggle_house_prices, kaggle_heart_disease, kaggle_march_mania, technique_tfdf, technique_realmlp_catboost_xgb, concept_log_loss_calibration [INFERRED 0.85]
- **Groq + Llama 3.3 70B form the sentiment inference backbone of AutoTrader's 15-min scan loop** — wiki_tools_groq_tool, wiki_models_llama_3_3_70b, wiki_tools_groq_autotrader_use, llama_sentiment_use, llama_cost_rationale, wiki_tools_groq_latency_prop [EXTRACTED 0.95]

## Communities (35 total, 27 thin omitted)

### Community 0 - "Cameron's Kaggle Portfolio Overview — 14 Competitions"
Cohesion: 0.20
Nodes (19): Above-Ground Biomass Prediction from Satellite Imagery, Geospatial Flood Modelling (DEM, SAR, Physics-informed ML), IMO-Level Mathematical Reasoning (AIMO), Social Action Recognition in Mice (Behavioral Ethology), RNA 3D Structure Prediction (Structural Biology), AI Mathematical Olympiad — Progress Prize 3 ($2.2M), CSIRO — Image2Biomass Prediction, Google Tunix Hackathon — Train a Model to Show Its Work (+11 more)

### Community 1 - "Llama 3.3 70B — Meta Open-Weights LLM"
Cohesion: 0.18
Nodes (11): Llama 3.3 70B 128K Context Window, Rationale: Llama 70B ~10x Cheaper than GPT-4o for AutoTrader, Llama Model Family (1B/3B/8B/70B/405B), Llama 3.3 70B Sentiment Classification for AutoTrader, Ingest: ARC-AGI Benchmarking Harness, Ingest: AutoTrader Autonomous Paper Trading Bot, Ingest: Karpathy LLM Wiki Gist, Ingest: SofaScope AI-Powered Furniture Visual Search (+3 more)

### Community 2 - "Groq — LLM Inference API"
Cohesion: 0.20
Nodes (11): ARC-AGI Async LLM Test Harness, AutoTrader RSI+LLM Strategy, Cameron's Second Brain — Overview, Kaggle Competition Portfolio (14 competitions), Second Brain Knowledge System, SofaScope Visual Search System, Groq Usage in AutoTrader 15-Min Sentiment Loop, Groq Ultra-Low Latency Token Generation (+3 more)

### Community 3 - "Graphify Graph Report"
Cohesion: 0.20
Nodes (10): Community: AutoTrader Infrastructure, Community: Kaggle Portfolio, Community: Language & NLP Kaggle, Community: Wiki Core, Graph Fragmentation Metric (0.400 — 53 isolated nodes), God Node: Agentic Trading System Architecture (13 edges), God Node: wiki/index.md (14 edges — most connected), Hyperedge: Frontier Reasoning Benchmarks (AIMO + ARC-AGI + CoT) (+2 more)

### Community 4 - "ADR: Consensus-Based Memory Distillation"
Cohesion: 0.31
Nodes (10): Agentic Drift (hallucination compounding in memory), Open Question — Agentic Memory Retention Strategies, ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI, AutoTrader — Autonomous Paper Trading Bot, Deep Past — Akkadian Translation (Kaggle), LLM Review Pass Before Rotation, MBR Decoding (Minimum Bayes Risk), Provider Adapter Pattern (Multi-LLM) (+2 more)

### Community 5 - "Wiki Index — Master Catalog"
Cohesion: 0.19
Nodes (14): NCAA Bracket Prediction (March Mania), Log Loss and Calibration in Probabilistic Prediction, Predicting Heart Disease — Playground S6E2, House Prices — Advanced Regression Techniques (Rank ~19), March Machine Learning Mania 2026, RealMLP + CatBoost + XGBoost Ensemble, SHAP Analysis for Feature Importance, TensorFlow Decision Forests (TFDF) (+6 more)

### Community 6 - "CLAUDE.md — Wiki Schema & Workflows"
Cohesion: 0.60
Nodes (5): Graphify — Knowledge Graph Skill, LLM Wiki Pattern (Karpathy), Obsidian Integration, CLAUDE.md — Wiki Schema & Workflows, README — cameron-wiki

### Community 7 - "Jaguar Re-Identification Challenge"
Cohesion: 0.50
Nodes (5): Jaguar Re-Identification Challenge, SofaScope Production System, Cameron Kaggle Profile (raw source), CLIP+FAISS Embedding Retrieval, Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)

## Knowledge Gaps
- **69 isolated node(s):** `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool`, `ARC Prize 2025`, `Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Wiki Index — Master Catalog` connect `Wiki Index — Master Catalog` to `Cameron's Kaggle Portfolio Overview — 14 Competitions`, `Llama 3.3 70B — Meta Open-Weights LLM`, `Groq — LLM Inference API`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Groq — LLM Inference API` connect `Groq — LLM Inference API` to `Llama 3.3 70B — Meta Open-Weights LLM`, `Wiki Index — Master Catalog`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Ingest: Cameron's Kaggle Profile — 14 Competitions` connect `Cameron's Kaggle Portfolio Overview — 14 Competitions` to `Llama 3.3 70B — Meta Open-Weights LLM`, `Wiki Index — Master Catalog`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **What connects `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool` to the rest of the system?**
  _69 weakly-connected nodes found - possible documentation gaps or missing edges._