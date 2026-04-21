# Activity Log

Append-only chronological record of all wiki operations.
Format: `## [YYYY-MM-DD] operation | description`

---

## [2026-04-20] osint | ICS exploitability assessment — full evidence chain with attack surface documentation

Source: raw/osint/2026-04-19-scan-enriched.json + NIST NISTIR 7956 + CVE NVD + CISA advisories + vendor docs
Pages created:
  - wiki/open-questions/exploitability-assessment-2026-04-20.md
Pages updated: wiki/log.md

Key evidence confirmed:
  - BACnet WriteProperty: unauthenticated by ASHRAE 135 design (NIST NISTIR 7956)
  - CVE-2019-9569: buffer overflow in dactetra, RCE, build 571848 confirmed, McAfee/Trellix HVACking paper
  - CVE-2017-16748: Tridium Niagara ≤4.4 admin bypass via disabled account + blank password (Lahey Medical at 4.4.73.24 CONFIRMED vulnerable)
  - CVE-2018-12594: Reliable Controls MACH-ProWebCom unauthenticated GET to fileinfo.xml returns Master Password (v7.80 confirmed; v2.19.1 status uncertain)
  - Fortinet research confirmed: "full command and control without username/password" demonstrated against live boiler equipment
  - Attack difficulty: TRIVIAL for all devices — bacpypes pip install, 15 lines of Python, free BDT tool

---

## [2026-04-20] osint | ICS OSINT deep-dive — evidence verification pass (ARIN RDAP + web)

Source: raw/osint/2026-04-19-scan-enriched.json (re-analysis) + ARIN RDAP + web sources
Pages updated:
  - wiki/open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md (full evidence chain added)
  - wiki/open-questions/scottsboro-electric-power-board-2026-04-20.md (full evidence chain added)
  - wiki/open-questions/municipal-ics-cluster-2026-04-20.md (full evidence chain added)

Evidence confirmed via ARIN RDAP API and web sources (all passive):
  - 104.36.136.27 → City of Cartersville, CARTERSVILLE-FIBERCOM (AS64261)
    Contact: sgrier@cartersvillega.gov | Device = ClarenceBrownAHUs = Clarence Brown Conference Center (40,000 sq ft civic venue, 5450 GA Hwy 20)
  - 173.242.239.157/.158 → Scottsboro Electric Power Board (AS26809)
    Contact: sharp@sepb.net (ARIN unvalidated since Feb 2025) | TVA member utility, Survalent SCADA, 7 substations
  - 54.234.107.205 → AWS EC2 us-east-1, hostname ec2-54-234-107-205.compute-1.amazonaws.com (vanilla, no custom domain)
    Live BACnet FDT tunnel from this EC2 into Chicago boiler room (216.80.86.155, firmware 571848 = CVE-2019-9569 confirmed)
  - 12.5.26.10 → KIPP INSPIRED ACADEMY (AS, ARIN POC unvalidated since Oct 2016)
    Device Mitchell (DSC_1616E) aggregates 13 KIPP school building BACnet zones through one BBMD
  - 24.240.179.78 → Metro North Fire Protection District, 1815 Chambers Rd, St. Louis MO 63136 (name match confirmed)
  - 24.103.25.90 → City of Liberty MO water distribution tank (DSC_633E), peer BBMD at 24.39.116.210

---

## [2026-04-20] osint | ICS OSINT deep-dive — new critical infrastructure findings

Source: raw/osint/2026-04-19-scan-enriched.json (re-analysis)
Pages created:
  - wiki/open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  - wiki/open-questions/scottsboro-electric-power-board-2026-04-20.md
  - wiki/open-questions/municipal-ics-cluster-2026-04-20.md
Pages updated: wiki/log.md
Contradictions: None. These are new findings not previously profiled.

Key findings:
  - 4 hosts with Delta Controls firmware build 571848 = CONFIRMED CVE-2019-9569 vulnerable (CVSS 9.8)
    - 216.80.86.155 Chicago boiler room + AWS EC2 FDT tunnel (54.234.107.205, us-east-1)
    - 104.36.136.27 City of Cartersville, GA (municipal govt ASN AS64261) — ClarenceBrownAHUs
    - 64.62.4.194 Seattle — PT Elevator Access Control MASTER (physical security infrastructure)
    - 91.126.135.34 Barcelona — commercial building
  - AWS EC2 instance (54.234.107.205) maintaining live BACnet FDT tunnel into Chicago HVAC — possible remote mgmt or unauthorized C2
  - Scottsboro Electric Power Board (AS26809) — municipal electric utility's own ASN, 2x JCI NAE controllers internet-facing
  - 1700 Woodbourne Tank (Liberty, MO) — water distribution tank controller, peer BBMD on second Charter IP
  - Chambers Firehouse (Florissant, MO) — fire station HVAC on internet, same St. Louis metro as WalkerMedical
  - St. Louis metro cluster now 4 sectors: medical, commercial, emergency services, education

---

## [2026-04-18] ingest | Hull Tactical competition data — Kaggle API pull

Source: raw/kaggle/hull-tactical-base-gateway.py, raw/kaggle/hull-tactical-relay.py, raw/kaggle/hull-tactical-data-schema.txt
Pages created: wiki/decisions/hull-tactical-strategy.md
Pages updated: wiki/kaggle/hull-tactical-market-prediction.md (confidence: low → high), wiki/index.md
Contradictions: none
Key findings:
  - Competition uses gRPC interactive evaluation API (not static CSV submission)
  - 94 anonymized features: D1–D9 (binary 0/1 regime flags) + E/I/M/P/S/V (continuous)
  - D features are structurally identical to AutoTrader's RSI threshold gate
  - Test set reveals lagged_forward_returns (yesterday's outcome) — enables online adaptation
  - 9,049 training days; test starts at date_id=8980
  - Early rows (date_id 0–~200): only D features are non-NaN (warm-up period)

---

## [2026-04-17] lint | First full lint pass + remediation

Issues found: 0 critical / 4 moderate / 4 low
Actions taken:
  - Fixed stale note in decisions/autotrader-decisions-log-retention.md (agentic-memory page falsely marked "not yet created")
  - Added consensus-based-memory-distillation + wiki-retention-policy wikilinks to open-questions/agentic-memory-retention-strategies.md
  - Added clip-faiss-visual-search wikilink to kaggle/jaguar-re-identification.md
Pages created (to resolve orphans and missing concepts):
  - wiki/kaggle/portfolio-overview.md (resolves 11 orphan Kaggle stubs in one shot)
  - wiki/tools/groq.md (Groq mentioned 4+ times, no page)
  - wiki/models/llama-3-3-70b.md (Llama 3.3 70B mentioned 4+ times, no page)
Pages updated: wiki/index.md
Orphans resolved: 11 of 12 (consensus-based-memory-distillation still weakly linked — acceptable)
Remaining moderate issues: consensus ADR weakly connected; Hull Tactical approach undocumented
Next lint recommended: after FLS ingests

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

---
## [2026-04-19] maintenance | Automated daily check

Run: 2026-04-19 01:11 UTC
Wiki pages: 49 | Raw sources: 6
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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
## [2026-04-19] maintenance | Automated daily check

Run: 2026-04-19 03:41 UTC
Wiki pages: 49 | Raw sources: 6
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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
## [2026-04-19] maintenance | Automated daily check

Run: 2026-04-19 06:05 UTC
Wiki pages: 49 | Raw sources: 6
Graph Fragmentation: 0.319

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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
## [2026-04-19] maintenance | Automated daily check

Run: 2026-04-19 09:03 UTC
Wiki pages: 49 | Raw sources: 6
Graph Fragmentation: 0.319

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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
## [2026-04-19] maintenance | Automated daily check

Run: 2026-04-19 13:20 UTC
Wiki pages: 49 | Raw sources: 6
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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
## [2026-04-19] maintenance | Automated daily check

Run: 2026-04-19 16:53 UTC
Wiki pages: 49 | Raw sources: 6
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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
## [2026-04-19] maintenance | Automated daily check

Run: 2026-04-19 20:49 UTC
Wiki pages: 49 | Raw sources: 6
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 00:31 UTC
Wiki pages: 49 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 1
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md
  [2026-04-17] trading/rsi-llm-signal-strategy.md
  [2026-04-17] trading/autotrader.md

Orphan pages (2):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md

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

## [2026-04-19] ingest | Shodan ICS Exposure Scan
Source: raw/osint/2026-04-19-scan-enriched.json
Pages created: [ics-exposure-2026-04-19.md]
Pages updated: [shodan-ics-osint.md]
Contradictions: none

## [2026-04-19] osint-analysis | BACnet BBMD Internet Exposure Deep Dive
Source: raw/osint/2026-04-19-scan-enriched.json
Pages created: [bacnet-bbmd-exposure-2026-04-19.md, walkermedical-disclosure-2026-04-19.md]
Pages updated: [ics-exposure-2026-04-19.md]
Contradictions: none
Key findings:
  - 84 internet-facing BACnet BBMDs in 1,000-host sample
  - 20+ Tridium Niagara hosts on pre-4.13 firmware (CVE-2021-22656/22657/44228)
  - KIPP Academy (12.5.26.10): single BBMD routing 13 school campuses
  - WalkerMedical (108.252.186.105): Delta Controls DSM_RTR V3.40 BBMD with active FDT entry at scan time, bridging internet to medical building BAS (surgery center, cancer center, DaVita dialysis). CVE-2019-9569 (CVSS 9.8) version-family match. Responsible disclosure report drafted.
  - Shriners Children's Hospital Charlotte (70.63.96.202): Tridium 4.11 on Charter residential ISP, three confirmed CVEs by version
  - Modbus CVE cluster: 39 Aliyun cloud VMs running SSH on port 502 — likely honeypots, not real ICS
  - DNP3 sample: 603/1000 hosts returned HTTP — mostly CDN/web false positives, not SCADA

---
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 01:47 UTC
Wiki pages: 51 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  open-questions/bacnet-bbmd-exposure-2026-04-19.md: [[ics-exposure-2026-04-19]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 3
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-19] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md

Orphan pages (3):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md

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
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 03:43 UTC
Wiki pages: 51 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  open-questions/bacnet-bbmd-exposure-2026-04-19.md: [[ics-exposure-2026-04-19]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 3
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-19] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md

Orphan pages (3):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md

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
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 06:24 UTC
Wiki pages: 51 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  open-questions/bacnet-bbmd-exposure-2026-04-19.md: [[ics-exposure-2026-04-19]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 3
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-19] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md

Orphan pages (3):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md

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
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 10:06 UTC
Wiki pages: 51 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  open-questions/bacnet-bbmd-exposure-2026-04-19.md: [[ics-exposure-2026-04-19]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 3
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-19] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md

Orphan pages (3):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md

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
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 14:05 UTC
Wiki pages: 51 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  open-questions/bacnet-bbmd-exposure-2026-04-19.md: [[ics-exposure-2026-04-19]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 3
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-19] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md

Orphan pages (3):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md

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
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 17:16 UTC
Wiki pages: 51 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  open-questions/bacnet-bbmd-exposure-2026-04-19.md: [[ics-exposure-2026-04-19]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 3
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-19] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md

Orphan pages (3):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md

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
## [2026-04-20] maintenance | Automated daily check

Run: 2026-04-20 20:58 UTC
Wiki pages: 51 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]
  open-questions/bacnet-bbmd-exposure-2026-04-19.md: [[ics-exposure-2026-04-19]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 3
  people: 1
  production-systems: 1
  techniques: 5
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-19] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-18] kaggle/hull-tactical-market-prediction.md
  [2026-04-18] kaggle/hull-tactical-lab.md
  [2026-04-18] decisions/hull-tactical-strategy.md

Orphan pages (3):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md

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
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 00:05 UTC
Wiki pages: 56 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 7
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md
  [2026-04-20] open-questions/municipal-ics-cluster-2026-04-20.md
  [2026-04-20] open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  [2026-04-19] techniques/shodan-ics-osint.md
  [2026-04-19] open-questions/walkermedical-disclosure-2026-04-19.md

Orphan pages (6):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 00:40 UTC
Wiki pages: 59 | Raw sources: 7
Graph Fragmentation: 0.319

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 10
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md
  [2026-04-20] open-questions/niagara-admin-capabilities-2026-04-20.md
  [2026-04-20] open-questions/municipal-ics-cluster-2026-04-20.md
  [2026-04-20] open-questions/exploitability-assessment-2026-04-20.md
  [2026-04-20] open-questions/disclosure-letters-2026-04-20.md

Orphan pages (9):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/disclosure-letters-2026-04-20.md
  open-questions/exploitability-assessment-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/niagara-admin-capabilities-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 03:36 UTC
Wiki pages: 59 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 10
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md
  [2026-04-20] open-questions/niagara-admin-capabilities-2026-04-20.md
  [2026-04-20] open-questions/municipal-ics-cluster-2026-04-20.md
  [2026-04-20] open-questions/exploitability-assessment-2026-04-20.md
  [2026-04-20] open-questions/disclosure-letters-2026-04-20.md

Orphan pages (9):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/disclosure-letters-2026-04-20.md
  open-questions/exploitability-assessment-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/niagara-admin-capabilities-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 06:09 UTC
Wiki pages: 59 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 10
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md
  [2026-04-20] open-questions/niagara-admin-capabilities-2026-04-20.md
  [2026-04-20] open-questions/municipal-ics-cluster-2026-04-20.md
  [2026-04-20] open-questions/exploitability-assessment-2026-04-20.md
  [2026-04-20] open-questions/disclosure-letters-2026-04-20.md

Orphan pages (9):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/disclosure-letters-2026-04-20.md
  open-questions/exploitability-assessment-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/niagara-admin-capabilities-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 09:47 UTC
Wiki pages: 59 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 10
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md
  [2026-04-20] open-questions/niagara-admin-capabilities-2026-04-20.md
  [2026-04-20] open-questions/municipal-ics-cluster-2026-04-20.md
  [2026-04-20] open-questions/exploitability-assessment-2026-04-20.md
  [2026-04-20] open-questions/disclosure-letters-2026-04-20.md

Orphan pages (9):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/disclosure-letters-2026-04-20.md
  open-questions/exploitability-assessment-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/niagara-admin-capabilities-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 12:22 UTC
Wiki pages: 59 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 10
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md
  [2026-04-20] open-questions/niagara-admin-capabilities-2026-04-20.md
  [2026-04-20] open-questions/municipal-ics-cluster-2026-04-20.md
  [2026-04-20] open-questions/exploitability-assessment-2026-04-20.md
  [2026-04-20] open-questions/disclosure-letters-2026-04-20.md

Orphan pages (9):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/bacnet-bbmd-exposure-2026-04-19.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/disclosure-letters-2026-04-20.md
  open-questions/exploitability-assessment-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/niagara-admin-capabilities-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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

## [2026-04-20] disclosure | KIPP St. Louis BACnet BBMD ("Mitchell")

Source: raw/osint/2026-04-19-scan-enriched.json
Pages created: wiki/open-questions/kipp-mitchell-disclosure-2026-04-20.md
Pages updated: wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md
Contradictions: corrected prior wiki entry — "KIPP Inspired Academy / 13-campus" → KIPP Inspire Academy (KIPP St. Louis network: 6 schools / ~2,700 students). Subnet count (13) is BACnet network segments, not 1:1 with campuses.
Key findings:
  - 12.5.26.10 (Delta Controls DSC-1616E "Mitchell") routes 13 internal BACnet subnets through one internet-facing BBMD
  - Single point of failure for 6-campus K-12 charter network (~2,700 students)
  - Wow framing: blast-radius — one internet action affects every campus simultaneously
  - K-12 building automation is asthma/heat/CO2-relevant safety infrastructure, not "comfort only"
  - Disclosure target: KIPP St. Louis (1310 Papin St Suite 203, 314-349-1388)
  - "Mitchell" is not a known KIPP campus name — likely integrator or building name; open question

---

## [2026-04-20] disclosure | Homanit Lietuva BACnet exposure (Pagiriai MDF/HDF plant)

Source: raw/osint/2026-04-19-scan-enriched.json
Pages created: wiki/open-questions/homanit-disclosure-2026-04-20.md
Pages updated: wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md
Contradictions: none
Key findings:
  - 85.206.88.54 (WAGO controller "Homanit.VAS_LNS_1") in Pagiriai, Vilniaus rajonas, Lithuania
  - Operator attribution high-confidence: device name carries operator name
  - MDF/HDF wood-fiberboard plant, 260,000 m³/yr capacity, ~€175M investment
  - Wow framing: combustible-dust regime (NFPA 664 / ATEX 2014/34/EU + 1999/92/EC)
  - Cannot confirm passively whether process-safety actuators are integrated to this BAS network — that distinction sets the impact ceiling
  - Disclosure path: Homanit Lietuva (info@homanit.lt) + German parent + WAGO PSIRT + NKSC (CERT-LT)

---

## [2026-04-20] correction | Shriners misidentification in BACnet survey page

Source: web verification (oasisshriners.org, shrinerschildrens.org/locations)
Pages updated: wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md
Contradictions: previous entry "Shriners Children's Hospital Charlotte" was incorrect. Device "Shriners_Oasis_10001" at 70.63.96.202 is the Oasis Shrine Temple (fraternal lodge / event venue, 604 Doug Mayes Pl, Charlotte NC 28262). Shriners Children's operates no hospital in Charlotte; nearest is Greenville SC. Pediatric patient-safety framing originally attached to this finding does not apply.
Resolution: in-place correction with explicit "Correction note" block in the BACnet survey page. No separate disclosure page filed for the Oasis exposure (downgraded — Niagara 4.11/Log4Shell exposure is real but lower severity than originally framed).

---

## [2026-04-20] update | Walker Medical disclosure — follow-up investigation plan appended

Source: existing wiki/open-questions/walkermedical-disclosure-2026-04-19.md
Pages updated: wiki/open-questions/walkermedical-disclosure-2026-04-19.md
Contradictions: flagged the unverified "same AT&T block" adjacency claim in the BACnet survey page (WalkerMedical 108.252.186.105 vs KIPP 12.5.26.10 — different address spaces; "same AS7018" is too weak a claim to repeat as "adjacent").
Key additions:
  - 6 follow-up investigation threads: identify 192.168.53.36, verify AT&T adjacency, Delta Controls firmware build cross-reference, Shodan history pivot, Wayback Machine pivot, BMS integrator identification
  - Cross-references to kipp-mitchell-disclosure-2026-04-20 and homanit-disclosure-2026-04-20

---


## [2026-04-21] analysis | Path B longitudinal — 12 external-FDT tunnel cases identified

Source: raw/osint/2026-04-20-scan-raw.json → raw/osint/2026-04-20-scan-enriched.json → raw/osint/2026-04-20-longitudinal.json
Pages created: wiki/open-questions/bacnet-fdt-external-tunnels-2026-04-21.md
Pages updated:
  - wiki/open-questions/homanit-disclosure-2026-04-20.md (cross-ref to aggregate page; "Homanit is not unique" note added)
  - wiki/open-questions/bacnet-bbmd-exposure-2026-04-19.md (2026-04-21 update block answering original open question about FDT prevalence; 94%/71% prevalence stats added)
Contradictions: none — extends prior findings.
Key additions:
  - Ran path B full Shodan collect → enrich → longitudinal. S7 credits exhausted (no S7 hosts); Modbus 1000 + BACnet 1000 + DNP3 300 collected.
  - Longitudinal seeded 17 BBMDs with any FDT entry; 16 had persistent tunnels (scan_count >= 3); 12 had external-public-IP FDT entries (the Homanit pattern).
  - Shared integrator endpoint discovered: 216.67.73.166 registered as Foreign Device for both 66.58.248.125 and 24.237.132.230, with identical 13-port rotation pattern over overlapping dates. Likely a single integrator bridging two client buildings.
  - Cloud-hosted BACnet clients observed across DigitalOcean (Homanit), AWS ca-central-1 (184.69.115.182), Azure East US (208.104.56.247) — an emerging class of cloud-VM-to-BACnet-building exposure.
  - Most-persistent case: 166.144.189.152 → 108.190.193.44, 275 scans across 37 rotating source ports. Most-scanned (internal-FDT): 104.36.136.27 → 10.21.175.238, 930 scans.
  - Queued 5 candidate per-target disclosures; not written yet pending Cameron review (per CLAUDE.md "never batch-write pages Cameron hasn't seen").
  - Fixed a Unicode/cp1252 crash in scripts/osint/longitudinal.py print statement (→ -> -->).

---

## [2026-04-21] update | KIPP and Homanit pages refreshed with path A longitudinal evidence

Source: raw/osint/2026-04-20-longitudinal.json
Pages updated:
  - wiki/open-questions/kipp-mitchell-disclosure-2026-04-20.md (FDT history section: 4 controllers registered over 47 days; .181 → .175 handoff on 2026-04-07 documented; FDT-vs-BDT distinction clarified; updated timeline)
  - wiki/open-questions/homanit-disclosure-2026-04-20.md (cross-reference to aggregate external-FDT findings page; broader-pattern note added without downgrading Homanit urgency)
Contradictions: none.

---

## [2026-04-21] security | Shodan API key rotation + history rewrite

Source: GitGuardian alert (secret detected in push to public repo)
Pages updated: (none — this is a repo-level incident, not a wiki content change)
Incident:
  - Commit 56bcdd2 "Add OSINT secret monitoring suite" (2026-04-20 21:19 from the other machine) hardcoded the Shodan API key in OSINT_README.md:100 as an `export SHODAN_API_KEY="..."` usage example.
  - Key was public on GitHub for ~12 hours before GitGuardian flagged it.
Response:
  - Rotated the Shodan key (done out of band by Cameron).
  - Redacted the literal key from OSINT_README.md HEAD; placeholder "your_shodan_api_key_here" substituted.
  - Added .claude/settings.local.json and *.local.json to .gitignore (settings.local.json can capture command-line args passed through Claude Code permission prompts).
  - Untracked .claude/settings.local.json from the index (kept on disk).
  - Scanned all incoming commits for other leaked secrets; only AWS's well-known dummy example AKIAIOSFODNN7EXAMPLE present — no additional real credentials.
  - `git filter-repo --replace-text` rewrote all history replacing the literal key with REDACTED_SHODAN_KEY.
  - `git push --force origin main` published the rewritten history. All commit SHAs on main rebuilt. The other machine(s) with clones of this repo must re-clone before their next push.
Lessons / preventive actions queued:
  - Enable GitHub's native secret scanning + push protection in repo Settings → Security.
  - Consider a pre-commit hook that runs gitleaks or trufflehog against staged content.
  - Document in CLAUDE.md: never pass secrets as command-line arguments to Claude Code (they are captured in .claude/settings.local.json via permission prompts).
  - Document: when wiring a new Shodan-using script, always source from .env, never hardcode in docs, examples, or tests.
Residual risk:
  - Old commit SHAs (56bcdd2 etc.) may still be reachable via direct URL on GitHub for up to ~90 days until GC.
  - Any fork, cache, or indexer that pulled before 2026-04-21 still has the old key in their history. The rotation (step 1) is what mitigates this.
Contradictions: none.

---

---
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 12:27 UTC
Wiki pages: 62 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 13
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-21] open-questions/homanit-disclosure-2026-04-20.md
  [2026-04-21] open-questions/bacnet-fdt-external-tunnels-2026-04-21.md
  [2026-04-21] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-20] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md

Orphan pages (8):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/disclosure-letters-2026-04-20.md
  open-questions/exploitability-assessment-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/niagara-admin-capabilities-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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
## [2026-04-21] maintenance | Automated daily check

Run: 2026-04-21 14:03 UTC
Wiki pages: 62 | Raw sources: 7
Graph Fragmentation: 0.310

Broken Links (🔴 CRITICAL):
  methodology/llm-wiki-pattern.md: [[wikilink]]

Pages by section:
  architectures: 2
  benchmarks: 1
  comparisons: 1
  decisions: 8
  integrations: 1
  interview-prep: 1
  kaggle: 17
  methodology: 2
  models: 3
  open-questions: 13
  people: 1
  production-systems: 1
  techniques: 6
  tools: 3
  trading: 2

Recently updated (last 7 days):
  [2026-04-21] open-questions/homanit-disclosure-2026-04-20.md
  [2026-04-21] open-questions/bacnet-fdt-external-tunnels-2026-04-21.md
  [2026-04-21] open-questions/bacnet-bbmd-exposure-2026-04-19.md
  [2026-04-20] open-questions/walkermedical-disclosure-2026-04-19.md
  [2026-04-20] open-questions/scottsboro-electric-power-board-2026-04-20.md

Orphan pages (8):
  kaggle/portfolio-overview.md
  models/llama-3-3-70b.md
  open-questions/cve-2019-9569-confirmed-hosts-2026-04-20.md
  open-questions/disclosure-letters-2026-04-20.md
  open-questions/exploitability-assessment-2026-04-20.md
  open-questions/municipal-ics-cluster-2026-04-20.md
  open-questions/niagara-admin-capabilities-2026-04-20.md
  open-questions/scottsboro-electric-power-board-2026-04-20.md

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
