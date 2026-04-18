# Graph Report - .  (2026-04-18)

## Corpus Check
- 50 files · ~25,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 123 nodes · 144 edges · 31 communities detected
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.79)
- Token cost: 11,400 input · 3,900 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Agentic Memory & Retention|Agentic Memory & Retention]]
- [[_COMMUNITY_Kaggle Portfolio|Kaggle Portfolio]]
- [[_COMMUNITY_AutoTrader Infrastructure|AutoTrader Infrastructure]]
- [[_COMMUNITY_Memory Distillation|Memory Distillation]]
- [[_COMMUNITY_Language & NLP Kaggle|Language & NLP Kaggle]]
- [[_COMMUNITY_Retention ADR Cluster|Retention ADR Cluster]]
- [[_COMMUNITY_Provider Adapter Pattern|Provider Adapter Pattern]]
- [[_COMMUNITY_Wiki Core|Wiki Core]]
- [[_COMMUNITY_Wiki Tooling|Wiki Tooling]]
- [[_COMMUNITY_SofaScope Visual Search|SofaScope Visual Search]]
- [[_COMMUNITY_Consensus Memory|Consensus Memory]]
- [[_COMMUNITY_FAISS Tool|FAISS Tool]]
- [[_COMMUNITY_ARC-AGI Reasoning|ARC-AGI Reasoning]]
- [[_COMMUNITY_ARC-AGI Harness|ARC-AGI Harness]]
- [[_COMMUNITY_LLM Wiki vs RAG|LLM Wiki vs RAG]]
- [[_COMMUNITY_LLM Wiki Pattern|LLM Wiki Pattern]]
- [[_COMMUNITY_Wiki Setup|Wiki Setup]]
- [[_COMMUNITY_CLIP Model|CLIP Model]]
- [[_COMMUNITY_Text Search ADR|Text Search ADR]]
- [[_COMMUNITY_Persistent Service ADR|Persistent Service ADR]]
- [[_COMMUNITY_Visual Search Interview|Visual Search Interview]]
- [[_COMMUNITY_Hybrid Search|Hybrid Search]]
- [[_COMMUNITY_Persistent Model Loading|Persistent Model Loading]]
- [[_COMMUNITY_SofaScope Raw|SofaScope Raw]]
- [[_COMMUNITY_Karpathy Gist Raw|Karpathy Gist Raw]]
- [[_COMMUNITY_Wiki Overview|Wiki Overview]]
- [[_COMMUNITY_Trading Architecture|Trading Architecture]]
- [[_COMMUNITY_Search Routing|Search Routing]]
- [[_COMMUNITY_ARC-AGI Benchmark|ARC-AGI Benchmark]]
- [[_COMMUNITY_ARC Prize 2025|ARC Prize 2025]]
- [[_COMMUNITY_ARC Benchmarking|ARC Benchmarking]]

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
- `Agentic Trading System Architecture` --references--> `AutoTrader README (raw)`  [EXTRACTED]
  wiki/architectures/agentic-trading-system.md → raw/repos/autotrader-readme.md
- `README — cameron-wiki` --references--> `CLAUDE.md — Wiki Schema & Workflows`  [EXTRACTED]
  README.md → CLAUDE.md
- `CLAUDE.md — Wiki Schema & Workflows` --references--> `LLM Wiki Pattern (Karpathy)`  [EXTRACTED]
  CLAUDE.md → wiki/methodology/llm-wiki-pattern.md

## Hyperedges (group relationships)
- **Consensus-Based Memory Distillation: MBR + LLM Review + Provider Adapters applied to agentic memory** — doc_consensus_memory_adr, concept_mbr_decoding, concept_llm_review_pass, concept_provider_adapter_pattern, concept_autotrader, concept_agentic_memory_retention [EXTRACTED 0.95]
- **LLM Wiki System: index + log + overview form the maintenance backbone of the wiki** — doc_index, doc_log, doc_overview, concept_llm_wiki_pattern, doc_claudemd [EXTRACTED 0.92]
- **Frontier reasoning benchmarks: AIMO + ARC-AGI + chain-of-thought as shared frontier ML challenge space** — doc_aimo_prize_3, concept_arc_agi, concept_chain_of_thought, concept_aimo_math_reasoning [INFERRED 0.75]
- **Tabular ML Kaggle competitions cluster — House Prices and Heart Disease both use gradient boosting on structured data** — kaggle_house_prices_regression, kaggle_playground_s6e2_heart_disease, technique_xgboost, technique_gradient_boosting_ensemble, concept_tabular_ml [INFERRED 0.85]
- **Computer vision wildlife competitions cluster — Jaguar Re-ID and MABe both involve animal visual recognition with embedding/contrastive methods** — kaggle_jaguar_reidentification, kaggle_mabe_mouse_behavior, technique_metric_learning, technique_clip_faiss, concept_computer_vision_kaggle [INFERRED 0.75]
- **LLM reasoning research cluster — Google Tunix, chain-of-thought, and process reward models form a coherent research direction** — kaggle_google_tunix_hackathon, technique_chain_of_thought [INFERRED 0.78]

## Communities

### Community 0 - "Agentic Memory & Retention"
Cohesion: 0.16
Nodes (25): ADR: 90-Day Rotating Retention for Trading Decisions Log, Agentic Drift (hallucination compounding in memory), Open Question — Agentic Memory Retention Strategies, Mathematical Olympiad / IMO-level Reasoning, ARC-AGI Benchmark, ADR: Custom Provider Adapters vs. LiteLLM for ARC-AGI, AutoTrader — Autonomous Paper Trading Bot, Chain-of-Thought Reasoning (o1-style) (+17 more)

### Community 1 - "Kaggle Portfolio"
Cohesion: 0.13
Nodes (21): Computer Vision (Kaggle competitions), Log Loss / Calibration (March Mania), Tabular ML (Kaggle), CSIRO — Image2Biomass Prediction, Google Tunix Hackathon, House Prices — Advanced Regression Techniques, Jaguar Re-Identification Challenge, MABe — Social Action Recognition in Mice (+13 more)

### Community 2 - "AutoTrader Infrastructure"
Cohesion: 0.13
Nodes (20): Agentic Trading System Architecture, Async Batch Runner (asyncio fan-out), Config-Driven Model Selection (models.yml), Cost Tracking at Model Level, HuggingFace Spaces Docker Deployment, Health Check as First-Class Concern, JSONL Persistent Feedback Loop, Per-Provider Rate Limiting (config-driven) (+12 more)

### Community 3 - "Memory Distillation"
Cohesion: 0.27
Nodes (12): Agentic Memory Compression via Distillation, AutoTrader Decisions-Log Retention (decisions.jsonl / outcomes.jsonl), MemGPT / Letta Tiered Memory, Quarterly Lint Pass (/lint workflow), Retain Outcomes / Rotate Reasoning Principle, Speculative Page Pruning (90-day staleness threshold), Weekly Review Pass (AutoTrader weekly_review.py), ADR: Wiki Retention Policy (+4 more)

### Community 4 - "Language & NLP Kaggle"
Cohesion: 0.5
Nodes (5): Deep Past: Akkadian Translation, Motion-S: Text-to-Sign Motion Generation, ByT5 (Byte-Level T5), LLM Review Pass Before Rotation, MBR Decoding (Minimum Bayes Risk)

### Community 5 - "Retention ADR Cluster"
Cohesion: 0.5
Nodes (4): ADR: 90-Day Rotating Retention for Trading Decisions Log, ADR: Wiki Retention Policy, Hull Tactical — Market Prediction, AutoTrader — Autonomous Paper Trading Bot

### Community 6 - "Provider Adapter Pattern"
Cohesion: 0.5
Nodes (4): Provider Adapter Pattern (Multi-LLM), ADR: Custom Provider Adapters vs. LiteLLM, Rationale for Custom Adapters, LiteLLM

### Community 7 - "Wiki Core"
Cohesion: 0.67
Nodes (3): cameron-wiki README, Wiki Index — Master Catalog, Activity Log — Append-Only Ingest History

### Community 8 - "Wiki Tooling"
Cohesion: 1.0
Nodes (3): Graphify — Knowledge Graph Skill, Obsidian Integration, CLAUDE.md — Wiki Schema & Workflows

### Community 9 - "SofaScope Visual Search"
Cohesion: 1.0
Nodes (3): SofaScope — AI-Powered Furniture Visual Search, CLIP + FAISS Visual Search Pipeline, Persistent Model Loading Pattern

### Community 10 - "Consensus Memory"
Cohesion: 0.67
Nodes (3): Consensus-Based Memory Distillation, LLM Review Pass, MBR Decoding

### Community 11 - "FAISS Tool"
Cohesion: 1.0
Nodes (1): FAISS Vector Search Tool

### Community 12 - "ARC-AGI Reasoning"
Cohesion: 1.0
Nodes (1): Abstract Reasoning (anti-memorization benchmark)

### Community 13 - "ARC-AGI Harness"
Cohesion: 1.0
Nodes (1): wiki/kaggle/arc-agi-benchmarking.md

### Community 14 - "LLM Wiki vs RAG"
Cohesion: 1.0
Nodes (1): LLM Wiki vs. RAG Comparison

### Community 15 - "LLM Wiki Pattern"
Cohesion: 1.0
Nodes (1): The LLM Wiki Pattern

### Community 16 - "Wiki Setup"
Cohesion: 1.0
Nodes (1): Cameron's Wiki Setup

### Community 17 - "CLIP Model"
Cohesion: 1.0
Nodes (1): CLIP Model

### Community 18 - "Text Search ADR"
Cohesion: 1.0
Nodes (1): ADR: Metadata Scoring vs. Embeddings for Text Search

### Community 19 - "Persistent Service ADR"
Cohesion: 1.0
Nodes (1): ADR: Persistent Service stdin/stdout vs. HTTP

### Community 20 - "Visual Search Interview"
Cohesion: 1.0
Nodes (1): System Design — Visual Search at Scale

### Community 21 - "Hybrid Search"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 22 - "Persistent Model Loading"
Cohesion: 1.0
Nodes (1): Persistent Model Loading Pattern

### Community 23 - "SofaScope Raw"
Cohesion: 1.0
Nodes (1): SofaScope README (raw)

### Community 24 - "Karpathy Gist Raw"
Cohesion: 1.0
Nodes (1): Karpathy LLM Wiki Gist (raw)

### Community 25 - "Wiki Overview"
Cohesion: 1.0
Nodes (1): Cameron's Second Brain — Overview

### Community 26 - "Trading Architecture"
Cohesion: 1.0
Nodes (1): Agentic Trading System Architecture

### Community 27 - "Search Routing"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 28 - "ARC-AGI Benchmark"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmark

### Community 29 - "ARC Prize 2025"
Cohesion: 1.0
Nodes (1): ARC Prize 2025

### Community 30 - "ARC Benchmarking"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmarking Harness

## Knowledge Gaps
- **53 isolated node(s):** `FAISS Vector Search Tool`, `Config-Driven Model Selection (models.yml)`, `Tenacity Exponential Backoff`, `Abstract Reasoning (anti-memorization benchmark)`, `wiki/kaggle/arc-agi-benchmarking.md` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `FAISS Tool`** (1 nodes): `FAISS Vector Search Tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ARC-AGI Reasoning`** (1 nodes): `Abstract Reasoning (anti-memorization benchmark)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ARC-AGI Harness`** (1 nodes): `wiki/kaggle/arc-agi-benchmarking.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `LLM Wiki vs RAG`** (1 nodes): `LLM Wiki vs. RAG Comparison`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `LLM Wiki Pattern`** (1 nodes): `The LLM Wiki Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wiki Setup`** (1 nodes): `Cameron's Wiki Setup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `CLIP Model`** (1 nodes): `CLIP Model`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Text Search ADR`** (1 nodes): `ADR: Metadata Scoring vs. Embeddings for Text Search`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persistent Service ADR`** (1 nodes): `ADR: Persistent Service stdin/stdout vs. HTTP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Visual Search Interview`** (1 nodes): `System Design — Visual Search at Scale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hybrid Search`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persistent Model Loading`** (1 nodes): `Persistent Model Loading Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `SofaScope Raw`** (1 nodes): `SofaScope README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Karpathy Gist Raw`** (1 nodes): `Karpathy LLM Wiki Gist (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Wiki Overview`** (1 nodes): `Cameron's Second Brain — Overview`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Trading Architecture`** (1 nodes): `Agentic Trading System Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Search Routing`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ARC-AGI Benchmark`** (1 nodes): `ARC-AGI Benchmark`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ARC Prize 2025`** (1 nodes): `ARC Prize 2025`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ARC Benchmarking`** (1 nodes): `ARC-AGI Benchmarking Harness`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Agentic Trading System Architecture` connect `AutoTrader Infrastructure` to `Retention ADR Cluster`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **What connects `FAISS Vector Search Tool`, `Config-Driven Model Selection (models.yml)`, `Tenacity Exponential Backoff` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Kaggle Portfolio` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._
- **Should `AutoTrader Infrastructure` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._