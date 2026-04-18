# Graph Report - .  (2026-04-18)

## Corpus Check
- Corpus is ~28,044 words - fits in a single context window. You may not need a graph.

## Summary
- 113 nodes · 129 edges · 35 communities detected
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.72)
- Token cost: 12,500 input · 4,200 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Concept Biomass Prediction|Concept Biomass Prediction]]
- [[_COMMUNITY_Groq Autotrader Use|Groq Autotrader Use]]
- [[_COMMUNITY_Concept Bracket Prediction|Concept Bracket Prediction]]
- [[_COMMUNITY_Concept Agentic Drift|Concept Agentic Drift]]
- [[_COMMUNITY_Graph Community Autotrader|Graph Community Autotrader]]
- [[_COMMUNITY_Overview Arc Agi Harness|Overview Arc Agi Harness]]
- [[_COMMUNITY_Concept Graphify|Concept Graphify]]
- [[_COMMUNITY_Kaggle Jaguar Reidentification|Kaggle Jaguar Reidentification]]
- [[_COMMUNITY_Tech Clip Faiss|Tech Clip Faiss]]
- [[_COMMUNITY_Tool Litellm|Tool Litellm]]
- [[_COMMUNITY_Tool Faiss|Tool Faiss]]
- [[_COMMUNITY_Kaggle Arc Prize 2025|Kaggle Arc Prize 2025]]
- [[_COMMUNITY_Kaggle Hull Tactical|Kaggle Hull Tactical]]
- [[_COMMUNITY_Kaggle Arc Agi Harness|Kaggle Arc Agi Harness]]
- [[_COMMUNITY_Concept Rag|Concept Rag]]
- [[_COMMUNITY_Method Cameron Wiki Setup|Method Cameron Wiki Setup]]
- [[_COMMUNITY_Arch Agentic Trading|Arch Agentic Trading]]
- [[_COMMUNITY_Model Clip|Model Clip]]
- [[_COMMUNITY_Model Byt5|Model Byt5]]
- [[_COMMUNITY_Concept Wiki Retention Policy|Concept Wiki Retention Policy]]
- [[_COMMUNITY_Decision Sofascope Metadata Vs Embedding|Decision Sofascope Metadata Vs Embedding]]
- [[_COMMUNITY_Decision Sofascope Stdin Stdout|Decision Sofascope Stdin Stdout]]
- [[_COMMUNITY_Concept Adr Log Retention|Concept Adr Log Retention]]
- [[_COMMUNITY_Decision Autotrader Open Model Vs Fronti|Decision Autotrader Open Model Vs Fronti]]
- [[_COMMUNITY_Integration Alpaca Api|Integration Alpaca Api]]
- [[_COMMUNITY_Interview Visual Search System Design|Interview Visual Search System Design]]
- [[_COMMUNITY_Concept Sofascope|Concept Sofascope]]
- [[_COMMUNITY_Concept Arc Agi|Concept Arc Agi]]
- [[_COMMUNITY_Person Andrej Karpathy|Person Andrej Karpathy]]
- [[_COMMUNITY_Trading Rsi Llm Signal Strategy|Trading Rsi Llm Signal Strategy]]
- [[_COMMUNITY_Tech Hybrid Routing|Tech Hybrid Routing]]
- [[_COMMUNITY_Raw Autotrader Readme|Raw Autotrader Readme]]
- [[_COMMUNITY_Raw Arc Agi Benchmarking Readme|Raw Arc Agi Benchmarking Readme]]
- [[_COMMUNITY_Raw Sofascope Readme|Raw Sofascope Readme]]
- [[_COMMUNITY_Raw Karpathy Llm Wiki|Raw Karpathy Llm Wiki]]

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
- `CSIRO — Image2Biomass Prediction` --semantically_similar_to--> `SofaScope Visual Search System`  [INFERRED] [semantically similar]
  wiki/kaggle/csiro-image2biomass.md → wiki/overview.md
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

### Community 0 - "Concept Biomass Prediction"
Cohesion: 0.2
Nodes (19): Above-Ground Biomass Prediction from Satellite Imagery, Geospatial Flood Modelling (DEM, SAR, Physics-informed ML), IMO-Level Mathematical Reasoning (AIMO), Social Action Recognition in Mice (Behavioral Ethology), RNA 3D Structure Prediction (Structural Biology), AI Mathematical Olympiad — Progress Prize 3 ($2.2M), CSIRO — Image2Biomass Prediction, Google Tunix Hackathon — Train a Model to Show Its Work (+11 more)

### Community 1 - "Groq Autotrader Use"
Cohesion: 0.14
Nodes (16): Groq Usage in AutoTrader 15-Min Sentiment Loop, Groq Ultra-Low Latency Token Generation, Groq LPU (Language Processing Unit) Hardware, Groq OpenAI-Compatible Chat Completions Endpoint, Groq — LLM Inference API, Llama 3.3 70B 128K Context Window, Llama 3.3 70B — Meta Open-Weights LLM, Rationale: Llama 70B ~10x Cheaper than GPT-4o for AutoTrader (+8 more)

### Community 2 - "Concept Bracket Prediction"
Cohesion: 0.19
Nodes (14): NCAA Bracket Prediction (March Mania), Log Loss and Calibration in Probabilistic Prediction, ARC-AGI Benchmark Page, AutoTrader Trading Bot Page, Kaggle Portfolio Overview Page, LLM Wiki Pattern (Karpathy) Page, Wiki Index — Master Catalog, SofaScope Production System Page (+6 more)

### Community 3 - "Concept Agentic Drift"
Cohesion: 0.31
Nodes (10): Agentic Drift (hallucination compounding in memory), Open Question — Agentic Memory Retention Strategies, ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI, AutoTrader — Autonomous Paper Trading Bot, Deep Past — Akkadian Translation (Kaggle), LLM Review Pass Before Rotation, MBR Decoding (Minimum Bayes Risk), Provider Adapter Pattern (Multi-LLM) (+2 more)

### Community 4 - "Graph Community Autotrader"
Cohesion: 0.2
Nodes (10): Community: AutoTrader Infrastructure, Community: Kaggle Portfolio, Community: Language & NLP Kaggle, Community: Wiki Core, Graph Fragmentation Metric (0.400 — 53 isolated nodes), God Node: Agentic Trading System Architecture (13 edges), God Node: wiki/index.md (14 edges — most connected), Hyperedge: Frontier Reasoning Benchmarks (AIMO + ARC-AGI + CoT) (+2 more)

### Community 5 - "Overview Arc Agi Harness"
Cohesion: 0.33
Nodes (6): ARC-AGI Async LLM Test Harness, AutoTrader RSI+LLM Strategy, Cameron's Second Brain — Overview, Kaggle Competition Portfolio (14 competitions), Second Brain Knowledge System, SofaScope Visual Search System

### Community 6 - "Concept Graphify"
Cohesion: 0.6
Nodes (5): Graphify — Knowledge Graph Skill, LLM Wiki Pattern (Karpathy), Obsidian Integration, CLAUDE.md — Wiki Schema & Workflows, README — cameron-wiki

### Community 7 - "Kaggle Jaguar Reidentification"
Cohesion: 0.5
Nodes (5): Jaguar Re-Identification Challenge, SofaScope Production System, Cameron Kaggle Profile (raw source), CLIP+FAISS Embedding Retrieval, Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)

### Community 8 - "Tech Clip Faiss"
Cohesion: 1.0
Nodes (2): CLIP + FAISS Visual Search Pipeline, Persistent Model Loading Pattern

### Community 9 - "Tool Litellm"
Cohesion: 1.0
Nodes (1): LiteLLM

### Community 10 - "Tool Faiss"
Cohesion: 1.0
Nodes (1): FAISS Vector Search Tool

### Community 11 - "Kaggle Arc Prize 2025"
Cohesion: 1.0
Nodes (1): ARC Prize 2025

### Community 12 - "Kaggle Hull Tactical"
Cohesion: 1.0
Nodes (1): Hull Tactical — Market Prediction

### Community 13 - "Kaggle Arc Agi Harness"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmarking Harness

### Community 14 - "Concept Rag"
Cohesion: 1.0
Nodes (1): Retrieval-Augmented Generation (RAG)

### Community 15 - "Method Cameron Wiki Setup"
Cohesion: 1.0
Nodes (1): Cameron's Wiki Setup

### Community 16 - "Arch Agentic Trading"
Cohesion: 1.0
Nodes (1): Agentic Trading System Architecture

### Community 17 - "Model Clip"
Cohesion: 1.0
Nodes (1): CLIP — Contrastive Language-Image Pretraining

### Community 18 - "Model Byt5"
Cohesion: 1.0
Nodes (1): ByT5 (Byte-Level T5)

### Community 19 - "Concept Wiki Retention Policy"
Cohesion: 1.0
Nodes (1): ADR: Wiki Retention Policy — Archive vs. Prune Speculative Pages

### Community 20 - "Decision Sofascope Metadata Vs Embedding"
Cohesion: 1.0
Nodes (1): ADR: Metadata Scoring vs. Embeddings for Text Search

### Community 21 - "Decision Sofascope Stdin Stdout"
Cohesion: 1.0
Nodes (1): ADR: Persistent Service stdin/stdout vs. HTTP

### Community 22 - "Concept Adr Log Retention"
Cohesion: 1.0
Nodes (1): ADR: 90-Day Rotating Retention for Trading Decisions Log

### Community 23 - "Decision Autotrader Open Model Vs Fronti"
Cohesion: 1.0
Nodes (1): ADR: Open Model vs. Frontier for Trading Sentiment

### Community 24 - "Integration Alpaca Api"
Cohesion: 1.0
Nodes (1): Alpaca API Integration

### Community 25 - "Interview Visual Search System Design"
Cohesion: 1.0
Nodes (1): System Design — Visual Search at Scale

### Community 26 - "Concept Sofascope"
Cohesion: 1.0
Nodes (1): SofaScope — AI-Powered Furniture Visual Search

### Community 27 - "Concept Arc Agi"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmark

### Community 28 - "Person Andrej Karpathy"
Cohesion: 1.0
Nodes (1): Andrej Karpathy

### Community 29 - "Trading Rsi Llm Signal Strategy"
Cohesion: 1.0
Nodes (1): RSI + LLM Signal Strategy

### Community 30 - "Tech Hybrid Routing"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 31 - "Raw Autotrader Readme"
Cohesion: 1.0
Nodes (1): AutoTrader README (raw)

### Community 32 - "Raw Arc Agi Benchmarking Readme"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmarking README (raw)

### Community 33 - "Raw Sofascope Readme"
Cohesion: 1.0
Nodes (1): SofaScope README (raw)

### Community 34 - "Raw Karpathy Llm Wiki"
Cohesion: 1.0
Nodes (1): Karpathy LLM Wiki Gist (raw)

## Knowledge Gaps
- **69 isolated node(s):** `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool`, `ARC Prize 2025`, `Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Tech Clip Faiss`** (2 nodes): `CLIP + FAISS Visual Search Pipeline`, `Persistent Model Loading Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tool Litellm`** (1 nodes): `LiteLLM`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tool Faiss`** (1 nodes): `FAISS Vector Search Tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kaggle Arc Prize 2025`** (1 nodes): `ARC Prize 2025`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kaggle Hull Tactical`** (1 nodes): `Hull Tactical — Market Prediction`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Kaggle Arc Agi Harness`** (1 nodes): `ARC-AGI Benchmarking Harness`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Concept Rag`** (1 nodes): `Retrieval-Augmented Generation (RAG)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Method Cameron Wiki Setup`** (1 nodes): `Cameron's Wiki Setup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Arch Agentic Trading`** (1 nodes): `Agentic Trading System Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Model Clip`** (1 nodes): `CLIP — Contrastive Language-Image Pretraining`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Model Byt5`** (1 nodes): `ByT5 (Byte-Level T5)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Concept Wiki Retention Policy`** (1 nodes): `ADR: Wiki Retention Policy — Archive vs. Prune Speculative Pages`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Decision Sofascope Metadata Vs Embedding`** (1 nodes): `ADR: Metadata Scoring vs. Embeddings for Text Search`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Decision Sofascope Stdin Stdout`** (1 nodes): `ADR: Persistent Service stdin/stdout vs. HTTP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Concept Adr Log Retention`** (1 nodes): `ADR: 90-Day Rotating Retention for Trading Decisions Log`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Decision Autotrader Open Model Vs Fronti`** (1 nodes): `ADR: Open Model vs. Frontier for Trading Sentiment`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Integration Alpaca Api`** (1 nodes): `Alpaca API Integration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Interview Visual Search System Design`** (1 nodes): `System Design — Visual Search at Scale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Concept Sofascope`** (1 nodes): `SofaScope — AI-Powered Furniture Visual Search`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Concept Arc Agi`** (1 nodes): `ARC-AGI Benchmark`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Person Andrej Karpathy`** (1 nodes): `Andrej Karpathy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Trading Rsi Llm Signal Strategy`** (1 nodes): `RSI + LLM Signal Strategy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tech Hybrid Routing`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Raw Autotrader Readme`** (1 nodes): `AutoTrader README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Raw Arc Agi Benchmarking Readme`** (1 nodes): `ARC-AGI Benchmarking README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Raw Sofascope Readme`** (1 nodes): `SofaScope README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Raw Karpathy Llm Wiki`** (1 nodes): `Karpathy LLM Wiki Gist (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Wiki Index — Master Catalog` connect `Concept Bracket Prediction` to `Concept Biomass Prediction`, `Groq Autotrader Use`, `Overview Arc Agi Harness`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Groq — LLM Inference API` connect `Groq Autotrader Use` to `Concept Bracket Prediction`, `Overview Arc Agi Harness`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Ingest: Cameron's Kaggle Profile — 14 Competitions` connect `Concept Biomass Prediction` to `Groq Autotrader Use`, `Concept Bracket Prediction`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **What connects `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool` to the rest of the system?**
  _69 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Groq Autotrader Use` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._