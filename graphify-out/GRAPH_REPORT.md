# Graph Report - .  (2026-04-17)

## Corpus Check
- 33 files · ~18,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 110 nodes · 217 edges · 10 communities detected
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 19 edges (avg confidence: 0.77)
- Token cost: 8,400 input · 4,600 output

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

## God Nodes (most connected - your core abstractions)
1. `Wiki Master Index` - 27 edges
2. `Agentic Trading System Architecture` - 21 edges
3. `Activity Log — Append-Only Ingest History` - 15 edges
4. `Wiki Index — Master Catalog` - 12 edges
5. `ARC-AGI Benchmarking Harness` - 12 edges
6. `Provider Adapter Pattern (Multi-LLM)` - 12 edges
7. `ADR: Custom Adapters vs. LiteLLM` - 10 edges
8. `ADR: Wiki Retention Policy` - 10 edges
9. `The LLM Wiki Pattern (Karpathy, April 2026)` - 9 edges
10. `LLM Wiki vs. RAG Comparison` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Retain Outcomes / Rotate Reasoning Principle` --semantically_similar_to--> `Memorization-Resistant Benchmarking`  [AMBIGUOUS] [semantically similar]
  wiki/decisions/wiki-retention-policy.md → wiki/benchmarks/arc-agi.md
- `Activity Log — Append-Only Ingest History` --references--> `raw/repos/karpathy-llm-wiki-gist.md`  [EXTRACTED]
  wiki/log.md → raw/repos/karpathy-llm-wiki-gist.md
- `SofaScope README (raw)` --references--> `SofaScope Production System`  [EXTRACTED]
  raw/repos/sofascope-ai-powered-product-match-finder.md → wiki/production-systems/sofascope.md
- `cameron-wiki README` --references--> `Activity Log — Append-Only Ingest History`  [EXTRACTED]
  README.md → wiki/log.md
- `CLAUDE.md — Wiki Schema and Workflows` --references--> `decisions/ ADR Directory — architectural decision records for interview prep`  [EXTRACTED]
  CLAUDE.md → wiki/methodology/cameron-wiki-setup.md

## Hyperedges (group relationships)
- **Agentic LLM Orchestration Systems** — arch_agentic_trading_system, kaggle_arc_agi_benchmarking, arch_provider_adapter_pattern, concept_async_batch_runner, concept_per_provider_rate_limiting, concept_config_driven_model_selection [INFERRED 0.85]
- **Agent Memory & Retention Policy Cluster** — concept_self_improvement_loop, technique_llm_review_pass, decision_autotrader_decisions_log_retention, decision_wiki_retention_policy, openq_agentic_memory_retention, concept_jsonl_feedback_loop [INFERRED 0.82]
- **SofaScope Visual Search System** — prod_sofascope, technique_clip_faiss_visual_search, technique_persistent_model_loading, technique_hybrid_search_routing, model_clip, tool_faiss, interview_visual_search_system_design [EXTRACTED 0.95]
- **Retention & Rotation System: wiki policy + LLM review technique + AutoTrader retention pattern form a unified memory management framework** — decision_wiki_retention_policy, technique_llm_review_pass_before_rotation, wiki_decisions_autotrader_decisions_log_retention, concept_quarterly_lint [EXTRACTED 0.95]
- **ARC-AGI Evaluation Stack: benchmark definition + benchmarking harness + provider adapter decision collectively realize Cameron's evaluation capability** — benchmark_arc_agi, decision_arc_agi_adapters_vs_litellm, wiki_kaggle_arc_agi_benchmarking, concept_provider_adapter_pattern [INFERRED 0.88]
- **Agentic Memory Cluster: LLM review pass technique + MemGPT tiered memory + wiki retention policy all participate in the broader problem of bounded, high-signal agent memory** — technique_llm_review_pass_before_rotation, concept_memgpt_tiered_memory, concept_agentic_memory_compression, wiki_open_questions_agentic_memory_retention [INFERRED 0.82]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (25): Agentic Trading System Architecture, HuggingFace Spaces Docker Deployment, Health Check as First-Class Concern, JSONL Persistent Feedback Loop, Persistent JSONL Feedback Loop — scan/log/review cycle for agentic self-improvement, Self-Improvement Loop Design, Single Entrypoint + Shared Lib Pattern, ADR: 90-Day Rotating Retention for Decisions Log (+17 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (21): Provider Adapter Pattern (Multi-LLM), ARC-AGI Benchmark, ARC-AGI Benchmark, Abstract Reasoning (anti-memorization benchmark), Async Batch Runner (asyncio fan-out), Config-Driven Model Selection (models.yml), Cost Tracking at Model Level, François Chollet (ARC-AGI creator) (+13 more)

### Community 2 - "Community 2"
Cohesion: 0.27
Nodes (12): Agentic Memory Compression via Distillation, AutoTrader Decisions-Log Retention (decisions.jsonl / outcomes.jsonl), MemGPT / Letta Tiered Memory, Quarterly Lint Pass (/lint workflow), Retain Outcomes / Rotate Reasoning Principle, Speculative Page Pruning (90-day staleness threshold), Weekly Review Pass (AutoTrader weekly_review.py), ADR: Wiki Retention Policy (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.31
Nodes (11): LLM Wiki vs. RAG Comparison, Index-First Query — read wiki/index.md before drilling into pages; avoids RAG infrastructure, LLM Wiki Pattern — compile at ingest, not query time, Field-Weighted Metadata Scoring — structured domain search without embeddings, RAG — Retrieval-Augmented Generation, Vannevar Bush's Memex (1945) — associative personal knowledge store, The LLM Wiki Pattern (Karpathy, April 2026), raw/repos/karpathy-llm-wiki-gist.md (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.49
Nodes (10): clip-vit-large-patch14 (768-dim CLIP model), DirectMetadataSearcher (field-weighted text search without embeddings), FAISS IndexFlatIP + L2 normalization (cosine similarity), Persistent subprocess stdin/stdout IPC pattern, SofaScope README (raw), System Design — Visual Search at Scale (SofaScope), SofaScope — AI-Powered Furniture Visual Search, CLIP + FAISS Visual Search Pipeline (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.4
Nodes (10): Alpaca Paper vs. Live Trading Environment, Dual-signal gating (both RSI and LLM sentiment must agree), Llama 3.3 70B via HuggingFace Inference API, Open model for high-frequency low-stakes inference (cost architecture principle), RSI (Relative Strength Index, 14-period, Wilder's smoothing), AutoTrader README (raw), ADR: Open Model vs. Frontier for Trading Sentiment, Alpaca API Integration (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.39
Nodes (8): L2-normalize + IndexFlatIP = cosine similarity (FAISS trick), Subprocess stdin/stdout IPC — persistent ML service communication pattern, ADR: Metadata Scoring vs. Embeddings for Text Search, ADR: Persistent Service stdin/stdout vs. HTTP, CLIP Model, SofaScope README (raw), FAISS Vector Search Tool, Activity Log — Append-Only Ingest History

### Community 7 - "Community 7"
Cohesion: 0.53
Nodes (6): CLAUDE.md — Wiki Schema and Workflows, decisions/ ADR Directory — architectural decision records for interview prep, Portfolio Extraction Workflow — sanitize fls-internal pages for public portfolio, Cameron's Wiki — Setup and Adaptations, cameron-wiki README, Wiki Index — Master Catalog

### Community 8 - "Community 8"
Cohesion: 0.6
Nodes (5): 90-Day Rotating Window — regime-aware retention heuristic for trading decisions, Intentional Forgetting in Agentic Systems — retain outcomes, rotate reasoning, ADR: 90-Day Rotating Retention for Trading Decisions Log, Open Question — Agentic Memory Retention Strategies, AutoTrader README (raw)

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (2): ARC-AGI LLM Baseline Benchmarking Harness, arc-agi-benchmarking README (raw)

## Ambiguous Edges - Review These
- `Retain Outcomes / Rotate Reasoning Principle` → `Memorization-Resistant Benchmarking`  [AMBIGUOUS]
  wiki/benchmarks/arc-agi.md · relation: semantically_similar_to

## Knowledge Gaps
- **21 isolated node(s):** `L2-normalize + IndexFlatIP = cosine similarity (FAISS trick)`, `Subprocess stdin/stdout IPC — persistent ML service communication pattern`, `arc-agi-benchmarking README (raw)`, `ARC-AGI LLM Baseline Benchmarking Harness`, `Karpathy LLM Wiki Gist (raw)` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (2 nodes): `ARC-AGI LLM Baseline Benchmarking Harness`, `arc-agi-benchmarking README (raw)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Retain Outcomes / Rotate Reasoning Principle` and `Memorization-Resistant Benchmarking`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **Why does `Wiki Master Index` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.334) - this node is a cross-community bridge._
- **Why does `Agentic Trading System Architecture` connect `Community 0` to `Community 8`, `Community 1`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `ADR: Wiki Retention Policy` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **What connects `L2-normalize + IndexFlatIP = cosine similarity (FAISS trick)`, `Subprocess stdin/stdout IPC — persistent ML service communication pattern`, `arc-agi-benchmarking README (raw)` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._