---
title: Overview
type: methodology
status: active
visibility: public
sources: []
related: [[wiki/index.md]], [[wiki/methodology/llm-wiki-pattern.md]]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [meta, overview, second-brain]
---

# Cameron's Second Brain — Overview

*This page is a high-level synthesis of everything in the wiki. Updated as knowledge accumulates.*

## Who this is for

Cameron Warren — IT/AI Systems professional at Furnitureland South (FLS) and CS student at UNC Charlotte, actively targeting AI/ML engineering and software development roles.

## What this wiki covers

This is a full second brain, not a narrow research wiki. It covers:

- **Production engineering work** at FLS: automation platforms, AI pipelines, search systems, enterprise chatbots
- **Kaggle competition work**: NLP, computer vision, scientific ML, memory-constrained data engineering
- **Research and learning**: papers, models, techniques, tools encountered in the job search and coursework
- **Career layer**: interview prep, architectural decisions, system design grounded in real production work
- **Experiments**: algorithmic trading concepts, local-first agentic systems

## Core thesis

Stop re-deriving. Start compiling. Knowledge accumulated in this wiki compounds with every ingest and every good question — unlike RAG, which rediscovers everything from scratch on every query. See [[wiki/comparisons/llm-wiki-vs-rag.md]] and [[wiki/methodology/llm-wiki-pattern.md]].

The pattern is Andrej Karpathy's LLM Wiki (April 2026) — see [[wiki/people/andrej-karpathy.md]]. It answers a problem Vannevar Bush identified in 1945: personal knowledge stores are only valuable if someone maintains the connections. The LLM handles that.

## Current knowledge state

- Sources ingested: 4
- Wiki pages: 19
- Last ingest: 2026-04-17 (ARC-AGI Benchmarking Harness)
- Last lint: never

## Strongest areas (so far)

- **Visual search systems** — SofaScope CLIP+FAISS pipeline fully documented with ADRs, technique pages, interview prep
- **Knowledge management methodology** — LLM Wiki pattern, RAG comparison, Cameron-specific setup
- **LLM evaluation infrastructure** — ARC-AGI harness with async concurrency, provider adapter pattern, cost tracking
- **Algorithmic trading** — AutoTrader RSI+LLM strategy, Alpaca integration, agentic feedback loop

## Known gaps

- FLS production systems (CRR, SellSmart, transcript pipeline) — deferred, will be ingested when docs are properly gathered
- Labs, datasets, people — mostly empty; will populate through future ingests
- ARC-AGI actual scores — harness is documented, but benchmark results not yet recorded
