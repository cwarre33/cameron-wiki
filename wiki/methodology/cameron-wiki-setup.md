---
title: Cameron's Wiki — Setup and Adaptations
type: methodology
status: active
visibility: public
sources: [raw/repos/karpathy-llm-wiki-gist.md]
related: [wiki/methodology/llm-wiki-pattern.md, wiki/comparisons/llm-wiki-vs-rag.md, wiki/overview.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [methodology, setup, second-brain, cameron-wiki, claude-code]
---

# Cameron's Wiki — Setup and Adaptations

How this wiki instantiates Karpathy's LLM Wiki pattern, and what was adapted for Cameron's broader context.

## Scope expansion: research wiki → full second brain

Karpathy's gist describes a research wiki. This wiki covers:
- **Production engineering** — FLS systems (CRR, SofaScope, SellSmart, transcript pipeline)
- **Kaggle competitions** — per-competition writeups, lessons, approaches
- **AI/ML research** — papers, models, techniques, tools
- **Career layer** — interview prep, ADRs, behavioral story bank
- **Trading experiments** — algo trading concepts, Alpaca integration
- **Coursework** — UNCC CS, AWS cert

The pattern is domain-agnostic (Karpathy explicitly says so). The expansion required a broader taxonomy but no changes to the core three-layer architecture.

## Key adaptations

### 1. Extended `raw/` taxonomy
Beyond the standard `papers/`, `blogs/`, `repos/` — added `fls-work/`, `kaggle/`, `trading/`, `coursework/`, `job-search/` to cover the full scope.

### 2. Extended `wiki/` taxonomy
Added beyond the standard structure:
- `production-systems/` — Cameron's FLS production work
- `integrations/` — Zendesk API, NetSuite/SuiteQL, AWS, MiCollab, Groq, Copilot Studio
- `decisions/` — ADRs: why approach X over Y (not in the original pattern; highest-value addition for interview prep)
- `kaggle/` — per-competition writeups
- `trading/` — algo trading concepts
- `interview-prep/` — system design notes tied to real work, behavioral story bank
- `methodology/` — meta-pages about this system (this page lives here)

### 3. Extended page frontmatter
Beyond the standard fields:
```yaml
status: active | archived | superseded   # tracks production lifecycle
visibility: public | private | fls-internal  # controls what gets published
```
`visibility: fls-internal` pages are never published without portfolio extraction + review.

### 4. Portfolio extraction workflow
Given any wiki page, generate a sanitized public version: strip `fls-internal` details, reframe as portfolio bullet, flag anything needing legal/HR review. Enables converting internal work into public portfolio material.

### 5. `decisions/` directory (ADRs)
Not in Karpathy's original pattern. Every time a non-obvious architectural or implementation decision is made, it gets an ADR page:
- What was decided
- What alternatives were considered
- Why this choice was made
- What tradeoffs were accepted
- Interview framing

This is the highest-ROI addition for Cameron's job search: each ADR is a pre-built behavioral story with technical depth.

## Runtime: Claude Code

Using Claude Code CLI as the runtime (as the PDF guide recommends). Claude Code reads `CLAUDE.md` automatically at session start — no need to manually instruct it to read the schema.

MCP servers configured in `.mcp.json`: fetch, brave-search, memory, github.

## What was NOT adapted from the PDF guide

- **Auto-ingestion pipeline** (RSS monitoring, cron jobs) — deferred until schema is proven
- **SQLite index** — not needed at current scale
- **arXiv MCP server** — deferred; most sources are internal docs and repos, not papers
- **Obsidian** — wiki lives in plain markdown; Obsidian is optional but compatible

## Scale expectations

Following Karpathy's observation that the compounding effect kicks in at ~10–20 ingested sources. The first 5 ingests establish the taxonomy in practice. First lint pass after ~10 sources will reveal what's working and what needs schema adjustment.

## See also

- [[wiki/methodology/llm-wiki-pattern.md]] — the original pattern this implements
- [[wiki/comparisons/llm-wiki-vs-rag.md]]
