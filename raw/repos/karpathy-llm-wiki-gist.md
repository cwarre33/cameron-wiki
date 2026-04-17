# LLM Wiki — Karpathy's Gist
Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
Author: Andrej Karpathy
Published: April 4, 2026 (updated 2026-04-17)
Fetched: 2026-04-17

---

# LLM Wiki

A pattern for building personal knowledge bases using LLMs.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

This can apply to a lot of different contexts:
- **Personal**: tracking goals, health, psychology, self-improvement
- **Research**: going deep on a topic over weeks or months
- **Reading a book**: filing each chapter, building out pages for characters, themes, plot threads
- **Business/team**: internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives**

## Architecture

Three layers:

**Raw sources** — immutable source documents. Articles, papers, images, data files. The LLM reads but never modifies them.

**The wiki** — LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, overview, synthesis. The LLM owns this layer entirely.

**The schema** — CLAUDE.md / AGENTS.md. Tells the LLM how the wiki is structured, conventions, and workflows. Co-evolved with the LLM over time.

## Operations

**Ingest.** Drop source into raw, tell LLM to process it. LLM reads, discusses takeaways, writes summary, updates index, updates entity/concept pages, appends to log. A single source might touch 10-15 wiki pages.

**Query.** Ask questions. LLM searches pages, reads, synthesizes with citations. Good answers get filed back as new wiki pages — comparisons, analyses, connections. Explorations compound in the knowledge base.

**Lint.** Health check: contradictions, stale claims, orphan pages, missing pages, missing cross-references, data gaps. LLM suggests new questions and sources.

## Indexing and logging

**index.md** — content-oriented catalog. Every page with link, one-line summary, optional metadata. Updated on every ingest. LLM reads this first on queries. Works well at ~100 sources, ~hundreds of pages without RAG infrastructure.

**log.md** — append-only chronological record. Prefix format: `## [YYYY-MM-DD] ingest | Title`. Parseable with grep.

## Optional: CLI tools

qmd (github.com/tobi/qmd) — local markdown search with BM25/vector hybrid search and LLM re-ranking. Has both CLI and MCP server.

## Tips and tricks

- **Obsidian Web Clipper** — browser extension, converts web articles to markdown
- **Download images locally** — Obsidian attachment folder + hotkey for local image storage
- **Obsidian graph view** — visualizes wiki shape, hubs, orphans
- **Marp** — markdown slide deck format, Obsidian plugin available
- **Dataview** — Obsidian plugin, queries over YAML frontmatter
- The wiki is just a git repo of markdown files

## Why this works

The tedious part of maintaining a knowledge base is the bookkeeping — updating cross-references, keeping summaries current, noting contradictions, maintaining consistency. Humans abandon wikis because maintenance burden grows faster than value. LLMs don't get bored, don't forget cross-references, can touch 15 files in one pass.

Related in spirit to Vannevar Bush's Memex (1945) — private, curated, associative trails between documents. Bush couldn't solve who does the maintenance. The LLM handles that.

## Note

Intentionally abstract — describes the idea, not a specific implementation. Directory structure, schema conventions, page formats, tooling all depend on domain and preferences. Everything is optional and modular.
