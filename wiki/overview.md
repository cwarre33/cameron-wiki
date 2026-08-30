---
title: Overview
type: methodology
status: active
visibility: public
sources: []
related: [[index]], [[methodology/llm-wiki-pattern.md]], [[work-log/2026-06-07-fls-catchup.md]]
created: 2026-04-17
updated: 2026-07-21
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

- Sources ingested: 8
- Wiki pages: 116
- Last maintenance: 2026-08-30 13:45 UTC


## Strongest areas (so far)

- **ClearView hosted inventory product** — Next.js + Entra SSO + ECS/Fargate + shared RDS delta sync + Approach export; initiative [[initiatives/flsp-103-inventory-lookup.md]] + hub [[production-systems/inventory-lookup-clearview.md]]
- **Zendesk automation platform** — CRR, dedicated agent, call transcripts, shared views, calendar, NS→ZD sync under [[initiatives/zendesk-automation-platform.md]]
- **Visual search systems** — SofaScope CLIP+FAISS pipeline with ADRs, technique pages, interview prep ([[production-systems/sofascope.md]])
- **SellSmart / Copilot** — DC Copilot program + Digital-to-Store agents ([[initiatives/sellsmart-program.md]], [[production-systems/digital-to-store-copilot.md]])
- **Knowledge management methodology** — LLM Wiki pattern, RAG comparison, Cameron-specific setup
- **LLM evaluation infrastructure** — ARC-AGI harness + Kimi agentic harness (TVC loop, benchmark gate)
- **Algorithmic trading** — AutoTrader RSI+LLM strategy, Alpaca integration, agentic feedback loop
- **Kaggle competition work** — all 14 competitions documented across NLP, bioinformatics, CV, math reasoning, trading, sports analytics, and wildlife ID
- **Security OSINT** — 6-tier credential discovery methodology, ICS exposure case studies, disclosure protocol ADRs

## Recent work (July 2026)

See [[work-log/2026-06-07-fls-catchup.md]] (May 21 → Jul 21) and [[work-log/2026-07-30-four-week-lookback.md]] (Jul 21 → Jul 30). Highlights:

- **ClearView Build Phase** — hosted product: AWS hosting, RDS parity, Entra SSO, Approach export
- **Public ClearView** — public ALB + WAF; Cloudflare CNAMEs verified ([[production-systems/clearview-public-alb-waf.md]])
- **Clarity + Admin Users + Mobile** — [[production-systems/clearview-clarity-telemetry.md]], [[production-systems/clearview-admin-users.md]], [[production-systems/clearview-mobile-ipad.md]]
- **Ops health** — parity PASS; ~$159/mo ([[production-systems/clearview-ops-health.md]])
- **Zendesk automation** — CRR, dedicated agent, supervisor exclusion

## Known gaps

- SellSmart NetSuite REST tool — still local WIP (uncommitted); not a tracker epic closeout
- ClearView open items — camera scan In Progress; ops-health parent Testing; Chrome-extension / Akeneo bugs; ECS autoscaling + post-launch hardening + order-list query
- SofaScope epic still Testing (most cluster Done-ish) — do not claim full production closeout
- Labs, datasets, people — mostly empty; will populate through future ingests
- Hull Tactical ($100k, deadline 2026-06-16) — outcome TBD
- Most Kaggle stubs lack notebook-level detail (Kaggle SPA blocks API content access)
- BusyLight OAuth refresh still open toward Oct 27, 2026