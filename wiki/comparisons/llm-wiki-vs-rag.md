---
title: LLM Wiki vs. RAG — Architectural Comparison
type: comparison
status: active
visibility: public
sources: [raw/repos/karpathy-llm-wiki-gist.md]
related: [wiki/methodology/llm-wiki-pattern.md, wiki/production-systems/sofascope.md, wiki/techniques/clip-faiss-visual-search.md, wiki/interview-prep/system-design-visual-search.md]
created: 2026-04-17
updated: 2026-04-17
confidence: high
tags: [rag, llm-wiki, knowledge-management, retrieval, comparison, architecture]
---

# LLM Wiki vs. RAG — Architectural Comparison

Two fundamentally different approaches to LLM + documents. Cameron has built production systems using both.

## Core contrast

| Dimension | RAG | LLM Wiki |
|-----------|-----|----------|
| When is intelligence applied? | Query time | Ingest time |
| What is stored? | Raw chunks + embeddings | Compiled, structured wiki articles |
| Cross-source synthesis | Re-derived every query | Pre-compiled, already there |
| Contradictions | Never flagged proactively | Flagged at ingest |
| Infrastructure | Vector DB, embedding model, retrieval pipeline | Plain markdown files + index |
| Scales by | Adding more chunks | Adding more wiki pages |
| Gets better over time? | No — same chunks, same retrieval | Yes — each ingest enriches existing pages |
| Human maintenance | Minimal (just add documents) | Curation + ingest workflow |
| Query latency | Embedding + retrieval + generation | Index lookup + file reads + generation |

## The fundamental difference

**RAG:** LLM is a reader at query time. It retrieves and synthesizes raw fragments on demand.

**LLM Wiki:** LLM is a writer at ingest time. It compiles knowledge into structured articles. At query time, it reads from compiled knowledge — not raw chunks.

Karpathy: *"The LLM is rediscovering knowledge from scratch on every question. There's no accumulation."*

## When RAG wins

- **Unstructured, high-volume corpora** — legal documents, customer support logs, codebases. Embedding-based retrieval handles fuzzy matching over large spaces better than index-based navigation.
- **Frequently updated sources** — if the underlying documents change constantly, the compilation overhead of wiki maintenance becomes costly.
- **Low-curation contexts** — when you can't afford to stay involved in ingesting each source.
- **Need for exact provenance** — RAG returns the original chunks with source attribution; the wiki synthesizes and may lose fine-grained provenance.

## When LLM Wiki wins

- **Compounding knowledge over time** — research, career knowledge, personal domain expertise
- **Cross-source synthesis is the primary value** — the wiki has already done the work of connecting five documents; RAG would redo it every query
- **Infrastructure simplicity** — no vector DB to maintain, no embedding API costs at query time
- **Structured, curated sources** — when you're choosing what goes in and staying involved in each ingest
- **Moderate scale** (~100 sources, ~hundreds of pages) — the index file is sufficient navigation

## Cameron's position: built both, different contexts

**Built RAG (SofaScope text search):** Tried embedding-based text search for a 200k furniture catalog. Replaced it with direct metadata scoring — 55× faster, zero cost, 92% accuracy. See [[wiki/decisions/sofascope-metadata-vs-embeddings.md]].

**Built RAG (LegalAssistant):** FAISS + HuggingFace embeddings + Groq LLM for legal document Q&A, with query rewriting and confidence scoring.

**Building LLM Wiki (this system):** Karpathy's pattern for a full second brain covering production work, research, career prep, and experiments.

The insight: **RAG is optimal for retrieval over unstructured corpora; the LLM Wiki is optimal for compiling and maintaining structured domain knowledge over time.** They're not competing — they serve different needs.

## Interview framing

"I've implemented retrieval systems in multiple contexts — FAISS-based visual similarity search, embedding-based legal document Q&A, and a metadata-scoring approach that outperformed embeddings for structured data. I've also built a personal knowledge base using the LLM Wiki pattern. The core tradeoff I think about is: when is intelligence better applied at ingest time (compile once, query cheaply) versus query time (flexible retrieval over raw sources)? The answer depends on how curated the corpus is, how often cross-source synthesis is needed, and how the system needs to scale."
