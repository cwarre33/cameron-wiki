---
title: "ADR: ClearView Location Movement Deferred (FLSP-401)"
type: decision
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_location_movement_deferred.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [adr, clearview, location, history, oracle-dw, flsp-401, furnitureland-south]
---

# ADR: ClearView Location Movement Deferred (FLSP-401)

## Decision

**Revert** the interim NetSuite location-level Item History movement build and **defer** campus/building-level movement until Oracle DW (or iSeries interim) can supply historical bin/building as-of each transaction.

## Context

FLSP-401 asked to "show location movement clearly." Stakeholders want **building-level** history (Mart / Outlet / Showroom). NetSuite cannot supply that history reliably: location names are too coarse; bin is mutable current-state; `systemnote` cannot be selectively queried/dumped; serial records lack a history field.

An interim location-level UI + migration `025` shipped then was **fully reverted** 2026-06-22 (code, `locations` table, `transaction_lines.location_name`, indexes, schema_migrations row).

## Options considered

| Option | Outcome |
|--------|---------|
| Ship NetSuite location-level movement | Misleading vs building-level goal; incomplete history |
| Probe NetSuite harder (`systemnote`, bins) | Technical dead-end (documented in SuiteQL KB + Jira comment) |
| **Defer to Oracle DW keyed on legacy serial FK** | Correct grain when DW finalizes |
| Interim iSeries/FLSPROD ODBC backfill | Fallback if DW slips — only if building-level needed sooner |

## Decision rationale

1. Wrong grain is worse than deferred feature for floor trust
2. Join key already exists: `inventorynumber.custitemnumber_fls_serialnn_id` → legacy serial — no NetSuite schema change required
3. Reverted SHA remains a UI reference for location-phrase rendering when rebuild starts

## Outcome

- FLSP-401 marked Done for the **shipped** (non-building) history work; building-level version explicitly deferred
- Resume path: DW (preferred) or iSeries ODBC via existing `iseries-odbc.ts`, join on `fls_serialnn_id` — **do not re-probe NetSuite for historical bin/building**
- Hub: [[production-systems/inventory-lookup-clearview.md]]
