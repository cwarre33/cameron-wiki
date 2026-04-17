---
title: "ADR: Wiki Retention Policy — When to Archive vs. Prune Speculative Pages"
type: decision
status: active
visibility: public
sources: []
related: [wiki/decisions/autotrader-decisions-log-retention.md, wiki/techniques/llm-review-pass-before-rotation.md, wiki/methodology/cameron-wiki-setup.md, wiki/open-questions/agentic-memory-retention-strategies.md]
created: 2026-04-17
updated: 2026-04-17
confidence: medium
tags: [adr, wiki, retention, memory, methodology, speculative]
---

# ADR: Wiki Retention Policy — When to Archive vs. Prune Speculative Pages

## Decision

Apply the same retain-outcomes-rotate-reasoning principle from [[wiki/decisions/autotrader-decisions-log-retention.md]] to this wiki itself:

| Page type | Retention rule |
|-----------|----------------|
| `confidence: high` — production systems, ADRs, techniques | Keep indefinitely. Mark `status: superseded` + link to successor rather than deleting. |
| `confidence: medium` — ingested research, models, tools | Keep indefinitely unless factually superseded. |
| `confidence: speculative` + no inbound wikilinks + >90 days stale | Candidate for pruning. Run LLM review pass first — distill any durable insight into a note on a related page, then delete. |
| `status: archived` | Keep forever. The record that something existed has value. |
| `wiki/log.md` entries | Keep forever. Append-only is the invariant; the log is an outcome record, not reasoning context. |

**Quarterly lint pass** replaces the daily_review equivalent. Every ~90 days: run `/lint`, identify speculative pages with no updates and no inbound links, distill before pruning.

## Rationale

**Why:** The graphify analysis of this wiki surfaced an open question from [[wiki/open-questions/agentic-memory-retention-strategies.md]]: *"Is `status: superseded` sufficient, or should speculative pages eventually be pruned?"*

The AutoTrader retention framework answers this directly:
- `decisions.jsonl` (reasoning context) → rotate on 90-day window
- `outcomes.jsonl` (results) → keep forever

Applied here:
- Speculative working notes = reasoning context → eligible for rotation after staleness threshold
- ADRs + production system pages + ingest summaries = outcomes → keep forever

**Why NOT just archive everything:** Archive pages accumulate indefinitely and add noise to graphify's knowledge graph. A pruned page is honestly absent; an archived page with stale speculative content misleads future queries.

**Why 90 days:** Matches AutoTrader's regime-change heuristic. For this wiki, "regime change" = a new job, a new project, or a new research direction. 90 days is long enough to decide whether a speculative idea has legs.

## The LLM review pass step

Before pruning any speculative page, run [[wiki/techniques/llm-review-pass-before-rotation.md]]:
1. Read the candidate page
2. Extract any durable claim not already covered in a related page
3. If a durable claim exists: append it to the most relevant existing page as a note
4. Then delete the speculative page and remove its entry from index.md

This mirrors AutoTrader's planned weekly review pass over `decisions.jsonl` — distill before purging.

## What this does NOT cover

- Pages actively being updated (no staleness threshold applies)
- `raw/` files — these are immutable by CLAUDE.md hard rule, never pruned
- Pages with inbound wikilinks — an orphan check is a prerequisite for pruning

## Open questions

- ⚠️ Should the 90-day staleness threshold be configurable per visibility level? (`fls-internal` pages may need shorter windows as context shifts.)
- Should graphify's orphan detection (nodes with 0 inbound edges) automate the candidate identification step?
