# cameron-wiki

Cameron Warren's second brain — a persistent, compounding knowledge base covering production engineering work, Kaggle competitions, AI/ML research, and career preparation.

Built on Andrej Karpathy's LLM Wiki pattern (April 2026): instead of re-deriving knowledge from raw sources on every query (RAG), the LLM compiles sources into an interlinked wiki of structured articles that only gets better over time.

## How it works

```
raw/        ← you add sources here (immutable after creation)
wiki/       ← the LLM maintains this (summaries, cross-references, synthesis)
CLAUDE.md   ← the contract: conventions, workflows, hard rules
```

Three operations keep the system running:

- **Ingest** — drop a source into `raw/`, Claude reads it, discusses takeaways, writes wiki pages, cross-links everything
- **Query** — ask a question, Claude consults the wiki and synthesizes an answer with citations; valuable answers get filed as new pages
- **Lint** — health check: contradictions, orphan pages, missing concepts, stale content, suggested investigations

## Using this wiki

Open Claude Code in this directory: `cd cameron-wiki && claude`

Claude reads `CLAUDE.md` automatically and knows the full schema, workflows, and hard rules.

## Structure

```
cameron-wiki/
├── CLAUDE.md                    # Schema and workflows
├── .mcp.json                    # MCP server config (fetch, brave-search, memory, github)
├── raw/                         # Immutable sources
│   ├── papers/                  # arXiv, research papers
│   ├── blogs/                   # AI lab blogs, engineering writeups
│   ├── repos/                   # GitHub READMEs
│   ├── models/                  # HuggingFace model cards
│   ├── videos/                  # YouTube transcripts
│   ├── datasets/
│   ├── fls-work/                # FLS internal docs (not published)
│   ├── kaggle/
│   ├── trading/
│   ├── coursework/
│   └── job-search/
└── wiki/                        # LLM-maintained knowledge
    ├── index.md                 # Master catalog
    ├── log.md                   # Append-only activity log
    ├── overview.md              # High-level synthesis
    ├── production-systems/      # CRR, SofaScope, SellSmart, transcript pipeline
    ├── architectures/
    ├── techniques/
    ├── integrations/
    ├── papers/
    ├── models/
    ├── benchmarks/
    ├── datasets/
    ├── tools/
    ├── labs/
    ├── people/
    ├── kaggle/
    ├── trading/
    ├── decisions/               # ADRs: why X over Y
    ├── interview-prep/
    ├── comparisons/
    ├── open-questions/
    └── methodology/
```

## MCP setup

Replace `REPLACE_ME` values in `.mcp.json`:
- `BRAVE_API_KEY` — get from brave.com/search/api
- `GITHUB_PERSONAL_ACCESS_TOKEN` — github.com/settings/tokens (read:repo scope)

## Visibility model

Every wiki page has a `visibility` field:
- `public` — safe for GitHub, portfolio, resume
- `private` — personal notes, not sensitive
- `fls-internal` — contains FLS proprietary details; sanitize before any publication

Run `portfolio extract [page]` to get a sanitized, publishable version of any page.
