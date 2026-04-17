---
title: The LLM Wiki Pattern (Karpathy, April 2026)
type: methodology
status: active
visibility: public
sources: [raw/repos/karpathy-llm-wiki-gist.md]
related: [wiki/methodology/cameron-wiki-setup.md, wiki/comparisons/llm-wiki-vs-rag.md, wiki/people/andrej-karpathy.md, wiki/overview.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [methodology, knowledge-management, rag, wiki, karpathy, memex, second-brain]
---

# The LLM Wiki Pattern (Karpathy, April 2026)

A pattern for building persistent, compounding personal knowledge bases using LLMs. Published April 4, 2026 as a GitHub gist by Andrej Karpathy. 5,000+ stars, ~3,000 forks in the first days.

## The core thesis

**RAG rediscovers knowledge from scratch on every query. The LLM Wiki compiles it once and keeps it current.**

Most LLM+documents systems (NotebookLM, ChatGPT file uploads, standard RAG) retrieve raw chunks at query time. Ask a question requiring five documents — the LLM finds and pieces together the fragments every time. Nothing accumulates.

The LLM Wiki inverts this: when a new source arrives, the LLM integrates it into a persistent wiki — updating entity pages, revising summaries, flagging contradictions, strengthening the synthesis. The next query finds compiled knowledge, not raw chunks. See [[wiki/comparisons/llm-wiki-vs-rag.md]].

## Intellectual lineage: Vannevar Bush's Memex (1945)

**This pattern is the first practical answer to a problem Vannevar Bush identified 80 years ago.**

Bush's 1945 essay "As We May Think" described the Memex: a personal, curated knowledge store with *associative trails* between documents — private, actively maintained, with the connections as valuable as the documents. Closer to this pattern than to what the web became.

Bush's unsolved problem: *who does the maintenance?* Updating cross-references, flagging contradictions, keeping summaries current as new material arrives — humans abandon wikis because the maintenance burden grows faster than the value.

**The LLM handles that.** It doesn't get bored, doesn't forget to update a cross-reference, can touch 15 files in one pass. The maintenance cost drops to near zero. Bush's vision becomes viable.

## Three-layer architecture

| Layer | Directory | Owner | Purpose |
|-------|-----------|-------|---------|
| Raw sources | `raw/` | Human | Immutable source documents — articles, papers, repos, images. LLM reads, never modifies |
| The wiki | `wiki/` | LLM | Generated markdown — summaries, entity pages, concept pages, comparisons, synthesis |
| The schema | `CLAUDE.md` | Both | Conventions, workflows, hard rules. Co-evolved with the LLM over time |

## Three operations

**Ingest** — drop source into `raw/`, tell the LLM to process it. LLM reads, discusses takeaways, writes summary, updates index, updates 5–15 related pages, appends to log. Stay involved: read the updates, guide emphasis.

**Query** — ask a question. LLM reads `index.md` first, drills into relevant pages, synthesizes with `[[wikilink]]` citations. **Critical:** good answers get filed back as new wiki pages (comparisons, analyses, connections). Explorations compound just like ingested sources.

**Lint** — periodic health check: contradictions, orphan pages, missing pages for frequently-mentioned concepts, stale content, weak sourcing, missing cross-references. LLM suggests next questions and sources.

## Index-first query: deliberately avoids RAG infrastructure

`wiki/index.md` is a content-oriented catalog — every page with link, one-line summary, and metadata. LLM reads this first on every query to find relevant pages, then drills in.

Karpathy: *"works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure."*

This is a principled choice, not a limitation. No vector database, no embeddings at query time, no infrastructure to maintain — plain markdown files navigated by index.

## The log's parseable prefix

```
## [YYYY-MM-DD] ingest | Source Title
## [YYYY-MM-DD] query | Question Asked
## [YYYY-MM-DD] lint | Health Check
```

`grep "^## \[" log.md` gives a full timeline. At 50+ ingests, auditing "what did I ingest in February?" or "when did I last lint?" becomes trivial.

## Division of labor

> *"You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions."* — Karpathy

> *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."* — Karpathy

The wiki is a software project. The artifact is structured knowledge. CLAUDE.md is the architecture doc — treat it with the same care.

## Why it compounds

Every ingest enriches 5–15 pages. Every good query answer becomes a new page. Every lint pass removes friction. The wiki is more useful at page 100 than page 10 — the opposite of a flat document collection, which degrades as it grows.

## See also

- [[wiki/methodology/cameron-wiki-setup.md]] — how this wiki instantiates the pattern
- [[wiki/comparisons/llm-wiki-vs-rag.md]] — the central architectural contrast
- [[wiki/people/andrej-karpathy.md]]
