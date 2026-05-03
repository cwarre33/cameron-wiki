# Graph Report - .  (2026-05-03)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 113 nodes · 129 edges · 36 communities detected
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
- [[_COMMUNITY_Community 35|Community 35]]

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

## Communities (36 total, 27 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.2
Nodes (19): Above-Ground Biomass Prediction from Satellite Imagery, Geospatial Flood Modelling (DEM, SAR, Physics-informed ML), IMO-Level Mathematical Reasoning (AIMO), Social Action Recognition in Mice (Behavioral Ethology), RNA 3D Structure Prediction (Structural Biology), AI Mathematical Olympiad — Progress Prize 3 ($2.2M), CSIRO — Image2Biomass Prediction, Google Tunix Hackathon — Train a Model to Show Its Work (+11 more)

### Community 1 - "Community 1"
Cohesion: 0.19
Nodes (14): NCAA Bracket Prediction (March Mania), Log Loss and Calibration in Probabilistic Prediction, ARC-AGI Benchmark Page, AutoTrader Trading Bot Page, Kaggle Portfolio Overview Page, LLM Wiki Pattern (Karpathy) Page, Wiki Index — Master Catalog, SofaScope Production System Page (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.22
Nodes (11): Groq Usage in AutoTrader 15-Min Sentiment Loop, Groq Ultra-Low Latency Token Generation, Groq LPU (Language Processing Unit) Hardware, Groq OpenAI-Compatible Chat Completions Endpoint, Groq — LLM Inference API, Llama 3.3 70B 128K Context Window, Llama 3.3 70B — Meta Open-Weights LLM, Rationale: Llama 70B ~10x Cheaper than GPT-4o for AutoTrader (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.31
Nodes (10): Agentic Drift (hallucination compounding in memory), Open Question — Agentic Memory Retention Strategies, ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI, AutoTrader — Autonomous Paper Trading Bot, Deep Past — Akkadian Translation (Kaggle), LLM Review Pass Before Rotation, MBR Decoding (Minimum Bayes Risk), Provider Adapter Pattern (Multi-LLM) (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.2
Nodes (10): Community: AutoTrader Infrastructure, Community: Kaggle Portfolio, Community: Language & NLP Kaggle, Community: Wiki Core, Graph Fragmentation Metric (0.400 — 53 isolated nodes), God Node: Agentic Trading System Architecture (13 edges), God Node: wiki/index.md (14 edges — most connected), Hyperedge: Frontier Reasoning Benchmarks (AIMO + ARC-AGI + CoT) (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (6): ARC-AGI Async LLM Test Harness, AutoTrader RSI+LLM Strategy, Cameron's Second Brain — Overview, Kaggle Competition Portfolio (14 competitions), Second Brain Knowledge System, SofaScope Visual Search System

### Community 6 - "Community 6"
Cohesion: 0.6
Nodes (5): Graphify — Knowledge Graph Skill, LLM Wiki Pattern (Karpathy), Obsidian Integration, CLAUDE.md — Wiki Schema & Workflows, README — cameron-wiki

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (5): Ingest: ARC-AGI Benchmarking Harness, Ingest: AutoTrader Autonomous Paper Trading Bot, Ingest: Karpathy LLM Wiki Gist, Ingest: SofaScope AI-Powered Furniture Visual Search, Wiki Activity Log — Append-Only

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (5): Jaguar Re-Identification Challenge, SofaScope Production System, Cameron Kaggle Profile (raw source), CLIP+FAISS Embedding Retrieval, Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)

## Knowledge Gaps
- **69 isolated node(s):** `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool`, `ARC Prize 2025`, `Metric Learning / Re-Identification (Contrastive/Triplet/ArcFace)` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Wiki Index — Master Catalog` connect `Community 1` to `Community 0`, `Community 2`, `Community 5`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Groq — LLM Inference API` connect `Community 2` to `Community 1`, `Community 5`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Ingest: Cameron's Kaggle Profile — 14 Competitions` connect `Community 0` to `Community 1`, `Community 7`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **What connects `README — cameron-wiki`, `LiteLLM`, `FAISS Vector Search Tool` to the rest of the system?**
  _69 weakly-connected nodes found - possible documentation gaps or missing edges._