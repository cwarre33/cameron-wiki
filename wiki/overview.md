---
title: Overview
type: methodology
status: active
visibility: public
sources: []
related: [[index]], [[methodology/llm-wiki-pattern.md]]
created: 2026-04-17
updated: 2026-05-20
confidence: high
tags: [meta, overview, second-brain]
---

# Cameron's Second Brain — Overview

*This page is a high-level synthesis of everything in the wiki. Updated as knowledge accumulates. See the [[index|Master Catalog]] for a full list of pages.*

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

- Sources ingested: 7
- Wiki pages: 83
- Last maintenance: 2026-07-03 21:16 UTC


## Strongest areas (so far)

- **Visual search systems** — SofaScope CLIP+FAISS pipeline fully documented with ADRs, technique pages, interview prep
- **FLS production engineering** — Inventory Lookup, pilot DB migration, Dedicated Agent, SellSmart Copilot, Zendesk returns reporting
- **Knowledge management methodology** — LLM Wiki pattern, RAG comparison, Cameron-specific setup
- **LLM evaluation infrastructure** — ARC-AGI harness + Kimi agentic harness (TVC loop, benchmark gate)
- **Algorithmic trading** — AutoTrader RSI+LLM strategy, Alpaca integration, agentic feedback loop
- **Kaggle competition work** — all 14 competitions documented across NLP, bioinformatics, CV, math reasoning, trading, sports analytics, and wildlife ID
- **Security OSINT** — 6-tier credential discovery methodology, ICS exposure case studies, disclosure protocol ADRs

## Recent work (May 2026)

See [[work-log/2026-05-period-summary.md]] for the full catch-up. Highlights:

- **Inventory Lookup / ClearView** — Next.js replacement for Review All Barcodes suitelet; sales feedback implemented (FLSP-159, FLSP-221)
- **Pilot database migration** — NetSuite + iSeries → Postgres one-time ETL spec and implementation (FLSP-232)
- **Dedicated Agent Assignment** — AWS Lambda + Zendesk webhook for CCS ticket routing (FLSP-163)
- **Customer sync spec** — SmartConnect → Task Server migration documented (FLSM-20)
- **auto-harness** — TVC agent loop with Ollama + 4 benchmark adapters (April; branch active)

## Known gaps

- **SellSmart Copilot REST tool** — ingested (WIP uncommitted in SellSmartTools)
- CRR deep-dive — still deferred
- Labs, datasets, people — mostly empty; will populate through future ingests
- Hull Tactical ($100k, deadline 2026-06-16) — active, outcome TBD
- Most Kaggle stubs lack notebook-level detail (Kaggle SPA blocks API content access)
- FLSM-20 Task Server implementation — spec only, code not started
