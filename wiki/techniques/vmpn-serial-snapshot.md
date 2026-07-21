---
title: VMPN Serial Snapshot (Grouped Browse)
type: technique
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp646_serial_snapshot.md
  - raw/fls-work/clearview-memory/2026-07-21/reference_vmpn_image_flags.md
  - raw/fls-work/clearview-memory/2026-07-21/project_shared_rds_dev_db.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[techniques/rds-delta-sync-watermarks.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [clearview, postgres, matview, vmpn, browse, performance, flsp-646, furnitureland-south]
---

# VMPN Serial Snapshot (Grouped Browse)

Technique for making ClearView's grouped-by-VMPN `/items` browse fast on a large Postgres serial table: **materialized snapshots + forced CTE materialization**, refreshed off the request path by delta sync.

**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]  
**Jira:** [FLSP-646](https://furniturelandsouth.atlassian.net/browse/FLSP-646) Done (under FLSP-391)

## Problem

Default grouped browse aggregates ~tens of thousands of VMPNs over ~1.3M snapshot/serial rows. Planner issues turned acceptable SQL into multi-second / multi-minute walls under concurrency on a memory-starved `db.t4g.small`.

## Techniques used

### 1. Default-browse matview (`vmpn_browse_default`)

- Serves the common unfiltered grouped path in ~150ms–1s (was ~11s live)
- Refreshed post-cycle by `sync-all-delta.ts` when transactions/serials lanes processed rows (~25–28s off request path)
- Read path: `isDefaultBrowse()` gate with live fallback; PGlite parity guard in `verify:ci`

### 2. Per-serial snapshot matview (`vmpn_serial_snapshot`)

- Populates a denormalized serial-level surface for filtered grouped browse
- Refresh ~52s per cycle — acceptable off-path

### 3. Force `AS MATERIALIZED` on heavy CTEs

Root cause of FLSP-646 perf miss: `vmpn_universe` CTE was **inlined** (PG12+) into a nested-loop left join and re-executed its ~210k-row aggregate once per outer row (~44×).

**Fix:** `AS MATERIALIZED` + `ANALYZE` after refresh → warm query ~11s → ~500ms for the snapshot statements; filtered browse ~10.4s → ~2.2s wall.

### 4. Expression / trigram indexes for real predicates

Queries filter with `UPPER(col) = UPPER($n)` and `ILIKE 'x%'` — plain btree on raw columns was unusable. Migration 035 added `UPPER(inv_tag_type)` btree + `fls_location_code` trigram.

### 5. Images-first ordering via `vmpn_image_flags`

Separate matview (migration 024): precomputed MPN has-image flag from four image sources. Live `UNION DISTINCT` over ~3.2M rows was ~10–12s and caused 3–17 min timeouts when inlined as correlated subqueries. Staleness affects **ordering only**, not correctness. See related image-flag refresh hooks on Akeneo / NS file / SofaScope loaders.

## Remaining levers

- Strict <1s wall AC needs **per-VMPN thumbnail precompute** (remaining ~1s is live thumbnail lookups shared with live path)
- Snapshot staleness signal (today: fallback on empty/missing, not on stale)
- Dev RDS right-size if concurrent capacity demands it — [[production-systems/clearview-rds-delta-sync.md]]

## When to apply

Use matview + `AS MATERIALIZED` + post-refresh `ANALYZE` when a browse aggregate is correct but the planner re-executes a large CTE per outer row. Pair with statement_timeout on the read pool so aborted HTTP clients cannot orphan long queries.
