# Graph Report - .  (2026-04-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 75 nodes · 61 edges · 30 communities detected
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.77)
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

## God Nodes (most connected - your core abstractions)
1. `Agentic Trading System Architecture` - 13 edges
2. `LLM Review Pass Before Rotation` - 8 edges
3. `ARC-AGI Benchmarking Harness` - 7 edges
4. `ADR: Wiki Retention Policy` - 7 edges
5. `Self-Improvement Loop Design` - 3 edges
6. `Speculative Page Pruning (90-day staleness threshold)` - 3 edges
7. `Quarterly Lint Pass (/lint workflow)` - 3 edges
8. `Agentic Memory Compression via Distillation` - 3 edges
9. `MBR Decoding (Minimum Bayes Risk)` - 3 edges
10. `Deep Past: Akkadian Translation` - 3 edges

## Surprising Connections (you probably didn't know these)
- `ARC-AGI Benchmarking Harness` --references--> `ARC-AGI Benchmarking README (raw)`  [EXTRACTED]
  wiki/kaggle/arc-agi-benchmarking.md → raw/repos/arc-agi-benchmarking-readme.md
- `ARC-AGI Benchmarking Harness` --semantically_similar_to--> `Agentic Trading System Architecture`  [INFERRED] [semantically similar]
  wiki/kaggle/arc-agi-benchmarking.md → wiki/architectures/agentic-trading-system.md
- `Cost Tracking at Model Level` --semantically_similar_to--> `ADR: Open Model vs. Frontier for Trading Sentiment`  [INFERRED] [semantically similar]
  wiki/kaggle/arc-agi-benchmarking.md → wiki/decisions/autotrader-open-model-vs-frontier.md
- `Agentic Trading System Architecture` --references--> `AutoTrader README (raw)`  [EXTRACTED]
  wiki/architectures/agentic-trading-system.md → raw/repos/autotrader-readme.md
- `cameron-wiki README` --references--> `Wiki Index — Master Catalog`  [EXTRACTED]
  README.md → wiki/index.md

## Hyperedges (group relationships)
- **Agentic LLM Orchestration Systems** — arch_agentic_trading_system, kaggle_arc_agi_benchmarking, arch_provider_adapter_pattern, concept_async_batch_runner, concept_per_provider_rate_limiting, concept_config_driven_model_selection [INFERRED 0.85]
- **Retention & Rotation System: wiki policy + LLM review technique + AutoTrader retention pattern form a unified memory management framework** — decision_wiki_retention_policy, technique_llm_review_pass_before_rotation, wiki_decisions_autotrader_decisions_log_retention, concept_quarterly_lint [EXTRACTED 0.95]
- **Agentic Memory Cluster: LLM review pass technique + MemGPT tiered memory + wiki retention policy all participate in the broader problem of bounded, high-signal agent memory** — technique_llm_review_pass_before_rotation, concept_memgpt_tiered_memory, concept_agentic_memory_compression, wiki_open_questions_agentic_memory_retention [INFERRED 0.82]
- **SofaScope Visual Search System** — prod_sofascope, tech_clip_faiss, tech_persistent_model, tech_hybrid_routing, model_clip [EXTRACTED 1.00]
- **Agent Memory & Retention Policy Cluster** — tech_llm_review, decision_autotrader_retention, decision_wiki_retention [INFERRED 0.85]
- **ARC-AGI Evaluation Stack** — benchmark_arc_agi, decision_arc_agi_adapters, kaggle_arc_agi_harness [INFERRED 0.90]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.19
Nodes (13): Agentic Trading System Architecture, HuggingFace Spaces Docker Deployment, Health Check as First-Class Concern, JSONL Persistent Feedback Loop, Self-Improvement Loop Design, Single Entrypoint + Shared Lib Pattern, ADR: 90-Day Rotating Retention for Decisions Log, ADR: Open Model vs. Frontier for Trading Sentiment (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.27
Nodes (12): Agentic Memory Compression via Distillation, AutoTrader Decisions-Log Retention (decisions.jsonl / outcomes.jsonl), MemGPT / Letta Tiered Memory, Quarterly Lint Pass (/lint workflow), Retain Outcomes / Rotate Reasoning Principle, Speculative Page Pruning (90-day staleness threshold), Weekly Review Pass (AutoTrader weekly_review.py), ADR: Wiki Retention Policy (+4 more)

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (7): Async Batch Runner (asyncio fan-out), Config-Driven Model Selection (models.yml), Cost Tracking at Model Level, Per-Provider Rate Limiting (config-driven), Tenacity Exponential Backoff, ARC-AGI Benchmarking Harness, ARC-AGI Benchmarking README (raw)

### Community 3 - "Community 3"
Cohesion: 0.5
Nodes (5): Deep Past: Akkadian Translation, Motion-S: Text-to-Sign Motion Generation, ByT5 (Byte-Level T5), LLM Review Pass Before Rotation, MBR Decoding (Minimum Bayes Risk)

### Community 4 - "Community 4"
Cohesion: 0.5
Nodes (4): ADR: 90-Day Rotating Retention for Trading Decisions Log, ADR: Wiki Retention Policy, Hull Tactical — Market Prediction, AutoTrader — Autonomous Paper Trading Bot

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (4): Provider Adapter Pattern (Multi-LLM), ADR: Custom Provider Adapters vs. LiteLLM, Rationale for Custom Adapters, LiteLLM

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (3): Consensus-Based Memory Distillation, LLM Review Pass, MBR Decoding

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (3): SofaScope — AI-Powered Furniture Visual Search, CLIP + FAISS Visual Search Pipeline, Persistent Model Loading Pattern

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (3): cameron-wiki README, Wiki Index — Master Catalog, Activity Log — Append-Only Ingest History

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): FAISS Vector Search Tool

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Abstract Reasoning (anti-memorization benchmark)

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): wiki/kaggle/arc-agi-benchmarking.md

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): LLM Wiki vs. RAG Comparison

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): The LLM Wiki Pattern

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Cameron's Wiki Setup

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): CLIP Model

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): ADR: Metadata Scoring vs. Embeddings for Text Search

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): ADR: Persistent Service stdin/stdout vs. HTTP

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): System Design — Visual Search at Scale

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Andrej Karpathy

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Persistent Model Loading Pattern

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (1): SofaScope README (raw)

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): Karpathy LLM Wiki Gist (raw)

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Cameron's Second Brain — Overview

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Agentic Trading System Architecture

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Hybrid Search Routing (Text + Image)

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmark

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): ARC Prize 2025

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): ARC-AGI Benchmarking Harness

## Knowledge Gaps
- **42 isolated node(s):** `FAISS Vector Search Tool`, `Config-Driven Model Selection (models.yml)`, `Tenacity Exponential Backoff`, `Abstract Reasoning (anti-memorization benchmark)`, `wiki/kaggle/arc-agi-benchmarking.md` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (1 nodes): `FAISS Vector Search Tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `Abstract Reasoning (anti-memorization benchmark)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `wiki/kaggle/arc-agi-benchmarking.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `LLM Wiki vs. RAG Comparison`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `The LLM Wiki Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Cameron's Wiki Setup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `CLIP Model`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `ADR: Metadata Scoring vs. Embeddings for Text Search`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `ADR: Persistent Service stdin/stdout vs. HTTP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `System Design — Visual Search at Scale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Andrej Karpathy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Persistent Model Loading Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `SofaScope README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `Karpathy LLM Wiki Gist (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Cameron's Second Brain — Overview`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Agentic Trading System Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Hybrid Search Routing (Text + Image)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `ARC-AGI Benchmark`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `ARC Prize 2025`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `ARC-AGI Benchmarking Harness`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Agentic Trading System Architecture` connect `Community 0` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `ARC-AGI Benchmarking Harness` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `AutoTrader — Autonomous Paper Trading Bot` connect `Community 4` to `Community 0`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **What connects `FAISS Vector Search Tool`, `Config-Driven Model Selection (models.yml)`, `Tenacity Exponential Backoff` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._