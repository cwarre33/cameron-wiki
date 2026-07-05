# Graph Report - .  (2026-07-05)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 113 nodes · 129 edges · 35 communities (8 shown, 27 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bd21d129`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Cameron's Kaggle Portfolio Overview — 14 Competitions|Cameron's Kaggle Portfolio Overview — 14 Competitions]]
- [[_COMMUNITY_Llama 3.3 70B — Meta Open-Weights LLM|Llama 3.3 70B — Meta Open-Weights LLM]]
- [[_COMMUNITY_Groq — LLM Inference API|Groq — LLM Inference API]]
- [[_COMMUNITY_Graphify Graph Report|Graphify Graph Report]]
- [[_COMMUNITY_ADR Consensus-Based Memory Distillation|ADR: Consensus-Based Memory Distillation]]
- [[_COMMUNITY_Wiki Index — Master Catalog|Wiki Index — Master Catalog]]
- [[_COMMUNITY_CLAUDE.md — Wiki Schema & Workflows|CLAUDE.md — Wiki Schema & Workflows]]
- [[_COMMUNITY_Jaguar Re-Identification Challenge|Jaguar Re-Identification Challenge]]
- [[_COMMUNITY_CLIP + FAISS Visual Search Pipeline|CLIP + FAISS Visual Search Pipeline]]
- [[_COMMUNITY_LiteLLM|LiteLLM]]
- [[_COMMUNITY_FAISS Vector Search Tool|FAISS Vector Search Tool]]
- [[_COMMUNITY_ARC Prize 2025|ARC Prize 2025]]
- [[_COMMUNITY_Hull Tactical — Market Prediction|Hull Tactical — Market Prediction]]
- [[_COMMUNITY_ARC-AGI Benchmarking Harness|ARC-AGI Benchmarking Harness]]
- [[_COMMUNITY_Retrieval-Augmented Generation (RAG)|Retrieval-Augmented Generation (RAG)]]
- [[_COMMUNITY_Cameron's Wiki Setup|Cameron's Wiki Setup]]
- [[_COMMUNITY_Agentic Trading System Architecture|Agentic Trading System Architecture]]
- [[_COMMUNITY_CLIP — Contrastive Language-Image Pretraining|CLIP — Contrastive Language-Image Pretraining]]
- [[_COMMUNITY_ByT5 (Byte-Level T5)|ByT5 (Byte-Level T5)]]
- [[_COMMUNITY_ADR Wiki Retention Policy — Archive vs. Prune Speculative Pages|ADR: Wiki Retention Policy — Archive vs. Prune Speculative Pages]]
- [[_COMMUNITY_ADR Metadata Scoring vs. Embeddings for Text Search|ADR: Metadata Scoring vs. Embeddings for Text Search]]
- [[_COMMUNITY_ADR Persistent Service stdinstdout vs. HTTP|ADR: Persistent Service stdin/stdout vs. HTTP]]
- [[_COMMUNITY_ADR 90-Day Rotating Retention for Trading Decisions Log|ADR: 90-Day Rotating Retention for Trading Decisions Log]]
- [[_COMMUNITY_ADR Open Model vs. Frontier for Trading Sentiment|ADR: Open Model vs. Frontier for Trading Sentiment]]
- [[_COMMUNITY_Alpaca API Integration|Alpaca API Integration]]
- [[_COMMUNITY_System Design — Visual Search at Scale|System Design — Visual Search at Scale]]
- [[_COMMUNITY_SofaScope — AI-Powered Furniture Visual Search|SofaScope — AI-Powered Furniture Visual Search]]
- [[_COMMUNITY_ARC-AGI Benchmark|ARC-AGI Benchmark]]
- [[_COMMUNITY_Andrej Karpathy|Andrej Karpathy]]
- [[_COMMUNITY_RSI + LLM Signal Strategy|RSI + LLM Signal Strategy]]
- [[_COMMUNITY_Hybrid Search Routing (Text + Image)|Hybrid Search Routing (Text + Image)]]
- [[_COMMUNITY_AutoTrader README (raw)|AutoTrader README (raw)]]
- [[_COMMUNITY_ARC-AGI Benchmarking README (raw)|ARC-AGI Benchmarking README (raw)]]
- [[_COMMUNITY_SofaScope README (raw)|SofaScope README (raw)]]
- [[_COMMUNITY_Karpathy LLM Wiki Gist (raw)|Karpathy LLM Wiki Gist (raw)]]

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

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **LLM Wiki System: index + log + overview form the maintenance backbone of the wiki** — doc_index, doc_log, doc_overview, concept_llm_wiki_pattern, doc_claudemd [EXTRACTED 0.92]
- **Computer vision wildlife competitions cluster — Jaguar Re-ID and MABe both involve animal visual recognition with embedding/contrastive methods** — kaggle_jaguar_reidentification, kaggle_mabe_mouse_behavior, technique_metric_learning, technique_clip_faiss, concept_computer_vision_kaggle [INFERRED 0.75]
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