# Cameron's Second Brain — Wiki Schema

Cameron Warren | IT/AI Systems @ Furnitureland South | CS student @ UNC Charlotte | AI/ML engineering job search

## Project structure

- `raw/` — immutable source material. **NEVER modify files here after initial creation.**
  - `raw/papers/` — arXiv papers and formal research
  - `raw/blogs/` — AI lab blogs, engineering writeups
  - `raw/repos/` — GitHub READMEs and OSS docs
  - `raw/models/` — Hugging Face model cards
  - `raw/videos/` — YouTube transcripts
  - `raw/datasets/` — dataset documentation
  - `raw/fls-work/` — internal FLS production system docs (docx → markdown, LaTeX, validation reports)
  - `raw/kaggle/` — competition overviews, notebooks, top solution writeups
  - `raw/trading/` — algo trading research, Alpaca docs, market structure
  - `raw/coursework/` — UNCC CS courses, AWS cert material
  - `raw/job-search/` — job descriptions, company research, interview prep sources
- `wiki/` — LLM-generated knowledge. The LLM owns this entirely.
  - `wiki/index.md` — master catalog. **Update on EVERY ingest.**
  - `wiki/log.md` — append-only activity log. **Never edit past entries.**
  - `wiki/overview.md` — high-level synthesis of all knowledge.
  - `wiki/methodology/` — meta-pages about this wiki system itself
  - `wiki/production-systems/` — Cameron's FLS production systems (CRR, SofaScope, SellSmart, transcript pipeline, etc.)
  - `wiki/architectures/` — serverless patterns, agent systems, transformer family, retrieval systems
  - `wiki/techniques/` — CLIP+FAISS, Whisper pipelines, RLHF, quantization, LoRA, routing algorithms, MBR decoding
  - `wiki/integrations/` — Zendesk API, NetSuite/SuiteQL, AWS, MiCollab, Groq, Copilot Studio quirks
  - `wiki/papers/` — formal published research summaries
  - `wiki/models/` — GPT, Claude, Llama, GPT-OSS-120B, ByT5, EVA-02, etc.
  - `wiki/benchmarks/` — MMLU, HumanEval, Kaggle leaderboards
  - `wiki/datasets/` — training data documentation
  - `wiki/tools/` — vLLM, PyTorch, FAISS, Ollama, Whisper, Groq SDK, transformers
  - `wiki/labs/` — OpenAI, Anthropic, DeepMind, DeepSeek, etc.
  - `wiki/people/` — researchers worth tracking
  - `wiki/kaggle/` — per-competition writeups: approach, lessons, what I'd do differently
  - `wiki/trading/` — strategies, Alpaca patterns, market concepts
  - `wiki/decisions/` — ADRs: WHY Cameron chose approach X over Y. Gold for interviews.
  - `wiki/interview-prep/` — system design notes tied to real work, behavioral story bank
  - `wiki/comparisons/` — synthesis pages filed from queries
  - `wiki/open-questions/` — gaps, next experiments, things to pursue

## Page conventions

Every wiki page MUST have YAML frontmatter:

```yaml
---
title: Page Title
type: architecture | technique | paper-summary | model | benchmark |
      dataset | tool | lab | person | comparison | open-question |
      production-system | integration | decision | kaggle-competition |
      trading-strategy | interview-note | methodology
status: active | archived | superseded
visibility: public | private | fls-internal
sources: [list of raw/ files referenced]
related: [list of wiki pages linked via wikilinks]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low | speculative
tags: [comma, separated, tags]
---
```

**Field guidance:**
- `status: archived` — system is no longer in production but knowledge is preserved
- `status: superseded` — replaced by a newer approach; link to successor page
- `visibility: public` — safe for GitHub, portfolio, resume
- `visibility: private` — personal notes, not sensitive but not portfolio material
- `visibility: fls-internal` — contains FLS proprietary details; never publish without sanitization

Use `[[wikilinks]]` for ALL cross-references between wiki pages.
**Bold key claims.** Mark speculative claims with ⚠️.

## Ingest workflow

When I say "ingest [source]":

1. Read the source in `raw/` (or fetch URL and save to `raw/` first — never skip saving)
2. Identify key claims, methods, results, decisions, and entities
3. **Discuss top 3–5 takeaways with Cameron BEFORE writing any wiki pages**
4. Wait for Cameron to confirm/refine, then proceed
5. Create/update a summary page in the appropriate `wiki/` subdirectory
6. Update ALL related concept, architecture, integration, and entity pages — a single source typically touches 5–15 pages
7. Add/strengthen `[[wikilinks]]` between affected pages
8. Flag any contradictions with existing wiki content explicitly — never silently overwrite
9. Update `wiki/index.md` with new/changed pages
10. Append entry to `wiki/log.md`:

```
## [YYYY-MM-DD] ingest | Source Title
Source: raw/path/to/file.md
Pages created: [list]
Pages updated: [list]
Contradictions: [none | description]
```

## Query workflow

When Cameron asks a question:

1. Read `wiki/index.md` to identify relevant pages
2. Read those pages (follow `[[wikilinks]]` as needed)
3. Synthesize answer with `[[wiki-link]]` citations to wiki pages
4. If the answer reveals a valuable synthesis, offer to file it as a new page in `wiki/comparisons/` or `wiki/open-questions/`
5. **NEVER answer from memory alone — always consult the wiki first**

## Lint workflow

When Cameron says "lint":

1. **Contradictions** — claims that conflict across pages 🔴
2. **Orphan pages** — no inbound `[[wikilinks]]` 🟡
3. **Missing pages** — concepts mentioned 3+ times without their own page 🟡
4. **Stale content** — not updated despite newer sources available 🟡
5. **Weak sourcing** — pages with only 1 source 🔵
6. **Missing cross-references** — related pages not linked 🔵
7. Suggest 5 questions worth investigating next
8. Suggest 3 sources worth adding next

Output a structured report with severity levels (🔴 critical / 🟡 moderate / 🔵 low).

## Portfolio extraction workflow

When Cameron says "portfolio extract [page]":

1. Read the target wiki page
2. Identify all `visibility: fls-internal` or `visibility: private` content
3. Produce a sanitized version that:
   - Replaces company-specific metrics with relative terms ("reduced latency by 97%") unless Cameron confirms they're public
   - Frames the work as a portfolio item or resume bullet
   - Preserves technical depth and decisions
   - Flags anything that needs legal/HR review before publishing with ⚠️ REVIEW BEFORE PUBLISH
4. Output as ready-to-use markdown (not saved — Cameron reviews first)

## Hard rules

- **NEVER modify files in `raw/` after initial creation**
- **NEVER answer a query from memory — always consult the wiki**
- **NEVER skip the "discuss takeaways first" step on ingests**
- **NEVER batch-write pages Cameron hasn't seen the structure of**
- If uncertain about a claim, mark it speculative with ⚠️
- If a source contradicts an existing page, flag it explicitly
- `wiki/index.md` must be updated on every ingest — no exceptions
- `wiki/log.md` is append-only — never edit or delete past entries

## MCP tools available

- **fetch** — grab web pages, blog posts, GitHub READMEs, documentation
- **brave-search** — search for papers, repos, blog posts (requires BRAVE_API_KEY)
- **memory** — track entities and relationships in knowledge graph across sessions
- **github** — fetch repo contents, READMEs, issues

## graphify skill

`/graphify` is available as a Claude Code skill (github.com/safishamsi/graphify).

**What it does:** Reads files in this repo, builds a persistent knowledge graph, returns structural relationships. 71.5× fewer tokens per query vs. reading raw files directly. Multimodal — handles markdown, PDFs, code, images, screenshots, audio/video (Whisper transcription). Honest about found vs. guessed relationships.

**Graph output lives in:** `.graph/` — committed to git, synced across machines. Other machines pull and immediately have the graph; no need to re-run from scratch.

**When to use graphify vs. wiki:**

| Use graphify when... | Use wiki when... |
|---------------------|-----------------|
| Exploring what's in `raw/` | Answering a specific question |
| Finding structural patterns across sources | Looking up a compiled synthesis |
| Discovering unexpected connections in source material | Citing a decision or technique |
| Session starts cold and wiki/index.md hasn't been read yet | Writing new wiki pages |

**Workflow: graphify → wiki:**
1. Run `/graphify` on `raw/` to surface structure and connections
2. Use graph output to identify which wiki pages need creating/updating
3. Write wiki pages with richer cross-references informed by the graph
4. The graph and wiki together are more powerful than either alone

**Installation (per machine):**
```bash
# In the cameron-wiki directory:
npx add-skill safishamsi/graphify
```
Then use `/graphify` in any Claude Code session opened from this directory.

## Obsidian integration

This vault is Obsidian-compatible out of the box. `[[wikilinks]]` render natively; graph view visualizes the full knowledge topology.

**Per-machine setup:**
1. Clone repo: `git clone https://github.com/cwarre33/cameron-wiki`
2. Open folder as Obsidian vault
3. Install community plugins: **Obsidian Git** (auto-sync), **Dataview** (frontmatter queries)
4. Obsidian Git: set auto-pull on startup, auto-commit+push interval

**Recommended Obsidian settings:**
- Attachment folder: `raw/assets/` (for Web Clipper downloads)
- New file location: `wiki/` (so new notes land in the right layer)
- Template folder: none (wiki pages are Claude-generated, not templated)

**Dataview query examples:**
```dataview
TABLE status, visibility, updated FROM "wiki/decisions" SORT updated DESC
TABLE status FROM "wiki/production-systems" WHERE status = "active"
LIST FROM "wiki" WHERE type = "open-question"
```
