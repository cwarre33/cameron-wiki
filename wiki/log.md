# Activity Log

Append-only chronological record of all wiki operations.
Format: `## [YYYY-MM-DD] operation | description`

---

## [2026-04-17] init | Wiki scaffold created

Source: N/A — initial setup
Pages created: wiki/index.md, wiki/log.md, wiki/overview.md
Pages updated: none
Notes: Full directory scaffold created. CLAUDE.md, .mcp.json, .gitignore, README.md written.
Taxonomy: raw/{papers,blogs,repos,models,videos,datasets,fls-work,kaggle,trading,coursework,job-search}
         wiki/{methodology,production-systems,architectures,techniques,integrations,papers,models,
               benchmarks,datasets,tools,labs,people,kaggle,trading,decisions,interview-prep,
               comparisons,open-questions}
Next: Ingest CRR documentation (source 1 of 5). FLS ingests deferred — gathering properly.

---

## [2026-04-17] ingest | SofaScope — AI-Powered Furniture Visual Search

Source: raw/repos/sofascope-ai-powered-product-match-finder.md
Pages created:
  - wiki/production-systems/sofascope.md
  - wiki/techniques/clip-faiss-visual-search.md
  - wiki/techniques/persistent-model-loading.md
  - wiki/techniques/hybrid-search-routing.md
  - wiki/decisions/sofascope-metadata-vs-embeddings.md
  - wiki/decisions/sofascope-persistent-service-stdin-stdout.md
  - wiki/tools/faiss.md
  - wiki/models/clip.md
  - wiki/interview-prep/system-design-visual-search.md
Pages updated: wiki/index.md
Contradictions: None. Note: docs cite "10,000+ products" but actual production scale is 200,000 — corrected in wiki, flagged in sofascope.md.

---

## [2026-04-17] ingest | Karpathy LLM Wiki Gist

Source: raw/repos/karpathy-llm-wiki-gist.md
Pages created:
  - wiki/methodology/llm-wiki-pattern.md
  - wiki/methodology/cameron-wiki-setup.md
  - wiki/comparisons/llm-wiki-vs-rag.md
  - wiki/people/andrej-karpathy.md
Pages updated: wiki/overview.md, wiki/index.md
Contradictions: None.

---

## [2026-04-17] ingest | Cameron's Kaggle Profile — all 14 competitions

Source: raw/kaggle/cameron-kaggle-profile.md (Kaggle API v1, Bearer token)
Pages created:
  - wiki/kaggle/deep-past-akkadian-translation.md
  - wiki/kaggle/motion-s-text-to-sign.md
  - wiki/kaggle/stanford-rna-3d-folding.md
  - wiki/kaggle/urban-flood-modelling.md
  - wiki/kaggle/hull-tactical-market-prediction.md
  - wiki/kaggle/arc-prize-2025.md
  - wiki/kaggle/aimo-progress-prize-3.md
  - wiki/kaggle/march-machine-learning-mania-2026.md
  - wiki/kaggle/playground-s6e2-heart-disease.md
  - wiki/kaggle/csiro-image2biomass.md
  - wiki/kaggle/jaguar-re-identification.md
  - wiki/kaggle/mabe-mouse-behavior.md
  - wiki/kaggle/google-tunix-hackathon.md
  - wiki/kaggle/house-prices-regression.md
  - wiki/techniques/mbr-decoding.md
  - wiki/models/byt5.md
Pages updated: wiki/index.md, wiki/overview.md
Contradictions: None.

Known rankings (from leaderboard API):
  - House Prices: rank ~19, RMSLE 0.00044 (perpetual competition, inflated leaderboard)
  - Motion-S: rank 25, score 0.43263 (2% below #1; active until 2026-05-10)
  - Urban Flood: rank 117, score 0.5304
  - Deep Past: outside top 200 (legit score 34.7); leakage exploit → 1st place (documented separately)
  - All others: outside top 200 or leaderboard unavailable

Notes:
  - Individual notebook content not available via Kaggle API (SPA-rendered pages)
  - Stubs based on notebook titles + leaderboard data + domain context
  - Hull Tactical ($100k) still active as of 2026-04-17

---
  - wiki/kaggle/motion-s-text-to-sign.md
  - wiki/kaggle/stanford-rna-3d-folding.md
  - wiki/kaggle/urban-flood-modelling.md
  - wiki/kaggle/hull-tactical-market-prediction.md
  - wiki/kaggle/arc-prize-2025.md
  - wiki/techniques/mbr-decoding.md
  - wiki/models/byt5.md
Pages updated: wiki/index.md, wiki/overview.md
Contradictions: None.
Notes:
  - 14 competitions entered, 47 notebooks. Confirmed ranks: Motion-S rank 25 (top 2%), Urban Flood rank 117.
  - Deep Past: ByT5+MBR legitimate score 34.7; separately found+documented data leakage → first place.
  - Hull Tactical ($100k) still active as of 2026-04-17.
  - Stanford RNA, AIMO, March Mania, Heart Disease, CSIRO, Jaguar Re-ID, MABe — entered but not yet fully documented.
  - Individual notebook content not available via API (SPA-rendered); stubs based on notebook titles + leaderboard data.

---

## [2026-04-17] ingest | ARC-AGI Benchmarking Harness

Source: raw/repos/arc-agi-benchmarking-readme.md
Pages created:
  - wiki/kaggle/arc-agi-benchmarking.md
  - wiki/benchmarks/arc-agi.md
  - wiki/architectures/provider-adapter-pattern.md
  - wiki/decisions/arc-agi-adapters-vs-litellm.md
Pages updated: wiki/index.md, wiki/overview.md
Contradictions: None.
Note: Harness is a fork of arcprizeorg/model_baseline. Supports ARC-AGI-1 and ARC-AGI-2. Actual benchmark scores not yet recorded — harness infrastructure documented only.

---

## [2026-04-17] ingest | AutoTrader — Autonomous Paper Trading Bot

Source: raw/repos/autotrader-readme.md
Pages created:
  - wiki/trading/autotrader.md
  - wiki/trading/rsi-llm-signal-strategy.md
  - wiki/decisions/autotrader-open-model-vs-frontier.md
  - wiki/decisions/autotrader-decisions-log-retention.md
  - wiki/integrations/alpaca-api.md
  - wiki/architectures/agentic-trading-system.md
  - wiki/open-questions/agentic-memory-retention-strategies.md
Pages updated: wiki/index.md
Contradictions: None.
Note: Self-improvement loop partially implemented — logging infrastructure exists, LLM review pass is a future enhancement.

---

## [2026-04-17] session | Obsidian + graphify setup; retention thread analysis; wiki optimization

Source: N/A — session synthesis
Pages created:
  - wiki/decisions/wiki-retention-policy.md
  - wiki/techniques/llm-review-pass-before-rotation.md
Pages updated:
  - wiki/architectures/agentic-trading-system.md (added provider-adapter-pattern + llm-review-pass wikilinks)
  - wiki/decisions/autotrader-decisions-log-retention.md (added retention cluster wikilinks)
  - wiki/interview-prep/system-design-visual-search.md (added arc-agi + arc-agi-benchmarking wikilinks)
  - wiki/index.md (added 2 new pages)
Graphify run: first full graph build — 54 nodes, 112 edges, 8 communities, 8.2× token reduction
Tools configured: graphify installed + symlinked to Claude Code; Obsidian vault opened with Git + Dataview plugins
Contradictions: None.
Notes:
  Graphify analysis surfaced: (1) wiki/log.md is the stealth hub (15 edges, bridges all 8 communities);
  (2) ARC-AGI community was orphaned in graph — 4 pages missed by detect (provider-adapter-pattern,
  benchmarks/arc-agi, arc-agi-adapters-vs-litellm, kaggle/arc-agi-benchmarking). Wikilinks added to
  connect ARC-AGI cluster into main body. Graphify --update needed to incorporate missing pages.
  (3) Retention thread: AutoTrader's retain-outcomes/rotate-reasoning principle applies directly to
  this wiki's own speculative page lifecycle — formalized as wiki-retention-policy ADR.
  (4) LLM review pass before rotation is the missing half of AutoTrader's self-improvement loop —
  documented as reusable technique.

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 21:29 UTC
Wiki pages: 27 | Raw sources: 5

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 2
  methodology: 2
  models: 1
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 4
  tools: 1
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md
  [2026-04-17] techniques/llm-review-pass-before-rotation.md

Orphan pages (3 — no inbound wikilinks):
  kaggle/deep-past-akkadian-translation.md
  techniques/hybrid-search-routing.md
  tools/faiss.md

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:12 UTC
Wiki pages: 34 | Raw sources: 5

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 1
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md
  [2026-04-17] techniques/mbr-decoding.md

Orphan pages (7 — no inbound wikilinks):
  kaggle/arc-prize-2025.md
  kaggle/hull-tactical-market-prediction.md
  kaggle/motion-s-text-to-sign.md
  kaggle/stanford-rna-3d-folding.md
  kaggle/urban-flood-modelling.md
  techniques/hybrid-search-routing.md
  tools/faiss.md

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:16 UTC
Wiki pages: 34 | Raw sources: 5

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 1
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md
  [2026-04-17] techniques/mbr-decoding.md

Orphan pages: none

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:18 UTC
Wiki pages: 35 | Raw sources: 5

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages: none

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:20 UTC
Wiki pages: 35 | Raw sources: 5

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages: none

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:28 UTC
Wiki pages: 35 | Raw sources: 5

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages: none

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:29 UTC
Wiki pages: 35 | Raw sources: 5

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages: none

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:30 UTC
Wiki pages: 35 | Raw sources: 5
Graph Fragmentation: 0.403

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages: none

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:33 UTC
Wiki pages: 35 | Raw sources: 5
Graph Fragmentation: 0.403

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 6
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages (3 — no inbound wikilinks):
  kaggle/motion-s-text-to-sign.md
  kaggle/stanford-rna-3d-folding.md
  kaggle/urban-flood-modelling.md

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:44 UTC
Wiki pages: 36 | Raw sources: 5

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  overview.md: [[wiki/index.md]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 7
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages (4):
  decisions/consensus-based-memory-distillation.md
  kaggle/motion-s-text-to-sign.md
  kaggle/stanford-rna-3d-folding.md
  kaggle/urban-flood-modelling.md

Suggested Links (Unlinked Mentions):
  architectures/agentic-trading-system.md: mention of 'alpaca-api'
  architectures/agentic-trading-system.md: mention of 'autotrader'
  architectures/agentic-trading-system.md: mention of 'autotrader-decisions-log-retention'
  architectures/agentic-trading-system.md: mention of 'autotrader-open-model-vs-frontier'
  architectures/agentic-trading-system.md: mention of 'llm-review-pass-before-rotation'
  architectures/agentic-trading-system.md: mention of 'provider-adapter-pattern'
  architectures/agentic-trading-system.md: mention of 'rsi-llm-signal-strategy'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi-benchmarking'
  benchmarks/arc-agi.md: mention of 'arc-agi-benchmarking'
  comparisons/llm-wiki-vs-rag.md: mention of 'clip-faiss-visual-search'
  comparisons/llm-wiki-vs-rag.md: mention of 'llm-wiki-pattern'
  comparisons/llm-wiki-vs-rag.md: mention of 'sofascope'
  comparisons/llm-wiki-vs-rag.md: mention of 'system-design-visual-search'
  decisions/arc-agi-adapters-vs-litellm.md: mention of 'arc-agi'

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:52 UTC
Wiki pages: 36 | Raw sources: 5
Graph Fragmentation: 0.400

Broken Links (🔴 CRITICAL):
  log.md: [[wiki/index.md]]
  log.md: [[wikilink]]
  methodology/llm-wiki-pattern.md: [[wikilink]]
  overview.md: [[wiki/index.md]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 7
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages (4):
  decisions/consensus-based-memory-distillation.md
  kaggle/motion-s-text-to-sign.md
  kaggle/stanford-rna-3d-folding.md
  kaggle/urban-flood-modelling.md

Suggested Links (Unlinked Mentions):
  architectures/agentic-trading-system.md: mention of 'alpaca-api'
  architectures/agentic-trading-system.md: mention of 'autotrader'
  architectures/agentic-trading-system.md: mention of 'autotrader-decisions-log-retention'
  architectures/agentic-trading-system.md: mention of 'autotrader-open-model-vs-frontier'
  architectures/agentic-trading-system.md: mention of 'llm-review-pass-before-rotation'
  architectures/agentic-trading-system.md: mention of 'provider-adapter-pattern'
  architectures/agentic-trading-system.md: mention of 'rsi-llm-signal-strategy'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi-benchmarking'
  benchmarks/arc-agi.md: mention of 'arc-agi-benchmarking'
  comparisons/llm-wiki-vs-rag.md: mention of 'clip-faiss-visual-search'
  comparisons/llm-wiki-vs-rag.md: mention of 'llm-wiki-pattern'
  comparisons/llm-wiki-vs-rag.md: mention of 'sofascope'
  comparisons/llm-wiki-vs-rag.md: mention of 'system-design-visual-search'
  decisions/arc-agi-adapters-vs-litellm.md: mention of 'arc-agi'

---
## [2026-04-17] maintenance | Automated daily check

Run: 2026-04-17 23:56 UTC
Wiki pages: 36 | Raw sources: 5
Graph Fragmentation: 0.400

Broken Links (🔴 CRITICAL):
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  methodology/llm-wiki-pattern.md: [[wikilink]]
  overview.md: [[wiki/index.md]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 7
  integrations: 1
  interview-prep: 1
  kaggle: 7
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 2
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/faiss.md
  [2026-04-17] techniques/persistent-model-loading.md

Orphan pages (4):
  decisions/consensus-based-memory-distillation.md
  kaggle/motion-s-text-to-sign.md
  kaggle/stanford-rna-3d-folding.md
  kaggle/urban-flood-modelling.md

Suggested Links (Unlinked Mentions):
  architectures/agentic-trading-system.md: mention of 'alpaca-api'
  architectures/agentic-trading-system.md: mention of 'autotrader'
  architectures/agentic-trading-system.md: mention of 'autotrader-decisions-log-retention'
  architectures/agentic-trading-system.md: mention of 'autotrader-open-model-vs-frontier'
  architectures/agentic-trading-system.md: mention of 'llm-review-pass-before-rotation'
  architectures/agentic-trading-system.md: mention of 'provider-adapter-pattern'
  architectures/agentic-trading-system.md: mention of 'rsi-llm-signal-strategy'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi-benchmarking'
  benchmarks/arc-agi.md: mention of 'arc-agi-benchmarking'
  comparisons/llm-wiki-vs-rag.md: mention of 'clip-faiss-visual-search'
  comparisons/llm-wiki-vs-rag.md: mention of 'llm-wiki-pattern'
  comparisons/llm-wiki-vs-rag.md: mention of 'sofascope'
  comparisons/llm-wiki-vs-rag.md: mention of 'system-design-visual-search'
  decisions/arc-agi-adapters-vs-litellm.md: mention of 'arc-agi'

---
## [2026-04-18] maintenance | Automated daily check

Run: 2026-04-18 01:33 UTC
Wiki pages: 46 | Raw sources: 5
Graph Fragmentation: 0.400

Broken Links (🔴 CRITICAL):
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wiki/index.md]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  log.md: [[wikilink]]
  methodology/llm-wiki-pattern.md: [[wikilink]]
  overview.md: [[index]]
  overview.md: [[index|Master Catalog]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 7
  integrations: 1
  interview-prep: 1
  kaggle: 16
  methodology: 2
  models: 2
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md
  [2026-04-17] tools/litellm.md
  [2026-04-17] tools/groq.md
  [2026-04-17] tools/faiss.md

Orphan pages (3):
  decisions/consensus-based-memory-distillation.md
  kaggle/portfolio-overview.md
  tools/groq.md

Suggested Links (Unlinked Mentions):
  architectures/agentic-trading-system.md: mention of 'alpaca-api'
  architectures/agentic-trading-system.md: mention of 'autotrader'
  architectures/agentic-trading-system.md: mention of 'autotrader-decisions-log-retention'
  architectures/agentic-trading-system.md: mention of 'autotrader-open-model-vs-frontier'
  architectures/agentic-trading-system.md: mention of 'llm-review-pass-before-rotation'
  architectures/agentic-trading-system.md: mention of 'provider-adapter-pattern'
  architectures/agentic-trading-system.md: mention of 'rsi-llm-signal-strategy'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi'
  architectures/provider-adapter-pattern.md: mention of 'arc-agi-benchmarking'
  benchmarks/arc-agi.md: mention of 'arc-agi-benchmarking'
  comparisons/llm-wiki-vs-rag.md: mention of 'clip-faiss-visual-search'
  comparisons/llm-wiki-vs-rag.md: mention of 'llm-wiki-pattern'
  comparisons/llm-wiki-vs-rag.md: mention of 'sofascope'
  comparisons/llm-wiki-vs-rag.md: mention of 'system-design-visual-search'
  decisions/arc-agi-adapters-vs-litellm.md: mention of 'arc-agi'
