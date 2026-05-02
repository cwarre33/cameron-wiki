# Graph Report - .  (2026-05-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 113 nodes · 129 edges · 35 communities detected
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.72)
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
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]

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
- **LLM Wiki System: index + log + overview form the maintenance backbone of the wiki** — doc_index, doc_log, doc_overview, concept_llm_wiki_pattern, doc_claudemd [EXTRACTED 0.92]
- **Computer vision wildlife competitions cluster — Jaguar Re-ID and MABe both involve animal visual recognition with embedding/contrastive methods** — kaggle_jaguar_reidentification, kaggle_mabe_mouse_behavior, technique_metric_learning, technique_clip_faiss, concept_computer_vision_kaggle [INFERRED 0.75]
- **Consensus-Based Memory Distillation: MBR + LLM Review + Provider Adapters applied to agentic memory** — doc_consensus_memory_adr, concept_mbr_decoding, concept_llm_review_pass, concept_provider_adapter_pattern, concept_autotrader, concept_agentic_memory_retention [EXTRACTED 0.95]
- **Scientific/Environmental ML Kaggle Cluster — Stanford RNA, Urban Flood, CSIRO Biomass** — kaggle_stanford_rna, kaggle_urban_flood, kaggle_csiro, technique_pseudo_labeling, concept_rna_folding, concept_flood_geospatial, concept_biomass_prediction [EXTRACTED 0.88]
- **Tabular ML Kaggle Cluster — House Prices + Heart Disease + March Mania use gradient boosting on structured data** — kaggle_house_prices, kaggle_heart_disease, kaggle_march_mania, technique_tfdf, technique_realmlp_catboost_xgb, concept_log_loss_calibration [INFERRED 0.85]
- **Groq + Llama 3.3 70B form the sentiment inference backbone of AutoTrader's 15-min scan loop** — groq_tool, llama_3_3_70b, groq_autotrader_use, llama_sentiment_use, llama_cost_rationale, groq_latency_prop [EXTRACTED 0.95]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.2
Nodes (19): Above-Ground Biomass Prediction from Satellite Imagery, Geospatial Flood Modelling (DEM, SAR, Physics-informed ML), IMO-Level Mathematical Reasoning (AIMO), Social Action Recognition in Mice (Behavioral Ethology), RNA 3D Structure Prediction (Structural Biology), AI Mathematical Olympiad — Progress Prize 3 ($2.2M), CSIRO — Image2Biomass Prediction, Google Tunix Hackathon — Train a Model to Show Its Work (+11 more)

### Community 1 - "Community 1"
Cohesion: 0.19
Nodes (14): NCAA Bracket Prediction (March Mania), Log Loss and Calibration in Probabilistic Prediction, ARC-AGI Benchmark Page, AutoTrader Trading Bot Page, Kaggle Portfolio Overview Page, LLM Wiki Pattern (Karpathy) Page, Wiki Index — Master Catalog, SofaScope Production System Page (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.18
Nodes (11): Llama 3.3 70B 128K Context Window, Llama 3.3 70B — Meta Open-Weights LLM, Rationale: Llama 70B ~10x Cheaper than GPT-4o for AutoTrader, Llama Model Family (1B/3B/8B/70B/405B), Llama 3.3 70B Sentiment Classification for AutoTrader, Ingest: ARC-AGI Benchmarking Harness, Ingest: AutoTrader Autonomous Paper Trading Bot, Ingest: Karpathy LLM Wiki Gist (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.2
Nodes (11): Groq Usage in AutoTrader 15-Min Sentiment Loop, Groq Ultra-Low Latency Token Generation, Groq LPU (Language Processing Unit) Hardware, Groq OpenAI-Compatible Chat Completions Endpoint, Groq — LLM Inference API, ARC-AGI Async LLM Test Harness, AutoTrader RSI+LLM Strategy, Cameron's Second Brain — Overview (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.31
Nodes (10): Agentic Drift (hallucination compounding in memory), Open Question — Agentic Memory Retention Strategies, ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI, AutoTrader — Autonomous Paper Trading Bot, Deep Past — Akkadian Translation (Kaggle), LLM Review Pass Before Rotation, MBR Decoding (Minimum Bayes Risk), Provider Adapter Pattern (Multi-LLM) (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.2
Nodes (10): Community: AutoTrader Infrastructure, Community: Kaggle Portfolio, Community: Language & NLP Kaggle, Community: Wiki Core, Graph Fragmentation Metric (0.400 — 53 isolated nodes), God Node: Agentic Trading System Architecture (13 edges), God Node: wiki/index.md (14 edges — most connected), Hyperedge: Frontier Reasoning Benchmarks (AIMO + ARC-AGI + CoT) (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.5
Nodes (5): Jaguar Re-Identification Challenge, SofaScope Production System, Cameron Kaggle Profile (raw source), CLIP+FAISS Embedding Retrieval, Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)

### Community 7 - "Community 7"
Cohesion: 0.6
Nodes (5): Graphify — Knowledge Graph Skill, LLM Wiki Pattern (Karpathy), Obsidian Integration, CLAUDE.md — Wiki Schema & Workflows, README — cameron-wiki

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (2): CLIP + FAISS Visual Search Pipeline, Persistent Model Loading Pattern

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): LiteLLM

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): FAISS Vector Search Tool

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): ARC Prize 2025

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Hull Tactical — Market Prediction

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmarking Harness

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Retrieval-Augmented Generation (RAG)

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Cameron's Wiki Setup

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): Agentic Trading System Architecture

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): CLIP — Contrastive Language-Image Pretraining

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): ByT5 (Byte-Level T5)

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): ADR: Wiki Retention Policy — Archive vs. Prune Speculative Pages

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): ADR: Metadata Scoring vs. Embeddings for Text Search

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): ADR: Persistent Service stdin/stdout vs. HTTP

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): ADR: 90-Day Rotating Retention for Trading Decisions Log

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): ADR: Open Model vs. Frontier for Trading Sentiment

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Alpaca API Integration

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): System Design — Visual Search at Scale

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): SofaScope — AI-Powered Furniture Visual Search

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmark

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Andrej Karpathy

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): RSI + LLM Signal Strategy

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): AutoTrader README (raw)

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmarking README (raw)

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): SofaScope README (raw)

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Karpathy LLM Wiki Gist (raw)

## Knowledge Gaps
- **69 isolated node(s):** `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool`, `ARC Prize 2025`, `Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 8`** (2 nodes): `CLIP + FAISS Visual Search Pipeline`, `Persistent Model Loading Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (1 nodes): `LiteLLM`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `FAISS Vector Search Tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `ARC Prize 2025`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Hull Tactical — Market Prediction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `ARC-AGI Benchmarking Harness`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Retrieval-Augmented Generation (RAG)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Cameron's Wiki Setup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `Agentic Trading System Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `CLIP — Contrastive Language-Image Pretraining`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `ByT5 (Byte-Level T5)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `ADR: Wiki Retention Policy — Archive vs. Prune Speculative Pages`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `ADR: Metadata Scoring vs. Embeddings for Text Search`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `ADR: Persistent Service stdin/stdout vs. HTTP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `ADR: 90-Day Rotating Retention for Trading Decisions Log`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `ADR: Open Model vs. Frontier for Trading Sentiment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Alpaca API Integration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `System Design — Visual Search at Scale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `SofaScope — AI-Powered Furniture Visual Search`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `ARC-AGI Benchmark`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Andrej Karpathy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `RSI + LLM Signal Strategy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `AutoTrader README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `ARC-AGI Benchmarking README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `SofaScope README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Karpathy LLM Wiki Gist (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Wiki Index — Master Catalog` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Groq — LLM Inference API` connect `Community 3` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Ingest: Cameron's Kaggle Profile — 14 Competitions` connect `Community 0` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **What connects `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool` to the rest of the system?**
  _69 weakly-connected nodes found - possible documentation gaps or missing edges._