---
title: ClearView RDS Delta Sync
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_shared_rds_dev_db.md
  - raw/fls-work/clearview-memory/2026-07-21/project_rds_delta_runner.md
  - raw/fls-work/clearview-memory/2026-07-21/project_delta_sync_build.md
  - raw/fls-work/clearview-memory/2026-07-21/project_full_scale_parity.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp547_txn_lane_drain.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp548_rds_parity_gap.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/pilot-database-migration.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[techniques/rds-delta-sync-watermarks.md]]"
  - "[[techniques/vmpn-serial-snapshot.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[integrations/netsuite-suitetalk-jwt.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [clearview, rds, postgres, delta-sync, netsuite, flsp-446, flsp-511, flsp-547, flsp-548, furnitureland-south]
---

# ClearView RDS Delta Sync

Shared Postgres RDS is ClearView's **read plane**: full ~23-year inventory history (~5GB), kept fresh by multi-lane SuiteQL delta sync from on-prem task servers.

**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]  
**Initiative:** [[initiatives/flsp-103-inventory-lookup.md]]  
**Historical ETL framing:** [[production-systems/pilot-database-migration.md]] (windowed pilot superseded by full-scale parity)

## Purpose

Floor staff browse/detail/orders against RDS (not live SuiteQL for every grid). NetSuite remains source of truth; delta lanes close the freshness gap on a scheduled cadence.

## Jira keys

| Key | Role | Status |
|-----|------|--------|
| [FLSP-446](https://furniturelandsouth.atlassian.net/browse/FLSP-446) | Shared AWS RDS Postgres | Done |
| [FLSP-511](https://furniturelandsouth.atlassian.net/browse/FLSP-511) | Automated delta runner | Done |
| [FLSP-547](https://furniturelandsouth.atlassian.net/browse/FLSP-547) | Transactions lane drain fix | Done |
| [FLSP-548](https://furniturelandsouth.atlassian.net/browse/FLSP-548) | Non-serial line parity | Done |
| [FLSP-391](https://furniturelandsouth.atlassian.net/browse/FLSP-391) | Data Sync and Performance parent | Testing |

## Architecture

### RDS footprint

- Postgres 16, private, KMS-encrypted, `rds.force_ssl=1` / app `sslmode=verify-full` with Amazon CA bundle
- **As-built placement:** PROD VPC (not FLS-STAGING) — STAGING site-to-site VPN was down and peering is non-transitive
- Dev: Single-AZ `db.t4g.small` gp3 50 GB; Prod: Multi-AZ `db.t4g.small`
- Roles: `app_rw` (app + sync DML), `sync_rw` alternate, `fls_admin` DDL only
- Topology context: [[integrations/fls-aws-topology.md]]

**Full-scale parity verified 2026-06-22** — not a date-windowed subset. Thereafter growth is delta-only.

### Multi-lane sync

`scripts/sync-all-delta.ts` runs lanes in dependency order with per-lane `sync_state` watermarks and failure isolation:

| Lane | Discover signal | Notes |
|------|-----------------|-------|
| transactions | `transaction.lastmodifieddate` | Broad item lines (serial + non-serial) after FLSP-548 |
| customers | lastmodified + **id-gap** from txns | Inactive included |
| notes | **id watermark** (`MAX(note.id)`) | `notedate`/`lastmodifieddate` not exposed on FLS role |
| cases | `supportcase.lastmodifieddate` | SuiteQL port of warranty extract |
| returns | RtnAuth lastmodified | Tiny return_inventory always re-pulled |
| serials | two-signal: `inventorynumber` + `inventorynumberlocation` | ~50% of changes are location-only |

Auth path for SuiteQL: [[integrations/netsuite-suitetalk-jwt.md]].

### Runner ops

- On-prem Windows Task Scheduler as `webadmin` — **not** in-cluster EventBridge/Lambda (deferred packaging)
- **2026-07-20:** combined multi-target `.bat` superseded by **one Scheduled Task per target** (`dev` / `staging` / `prod`) after a hang on one target blocked all three (~2 days)
- Cadence: **dev 30 min, staging 30 min, prod 15 min**
- CLI: `sync-all-delta.ts --target dev|staging|prod`

Watermark drain technique: [[techniques/rds-delta-sync-watermarks.md]]. Browse snapshot refresh: [[techniques/vmpn-serial-snapshot.md]].

## Hardening shipped

- **FLSP-547** — capped transactions lane had frozen watermark (no `ORDER BY`); drain-safe slice advances watermark to max LMD of processed slice
- **FLSP-548** — serial-bearing-only backfill left ~20% headers / ~33% lines gap; broad non-serial extract + backfill restored ≥100% item-bearing parity; on-demand `npm run parity:check` (daily email guard descaled)

## Open work / caveats

- Dev instance memory-starved for warm cache (`db.t4g.small` / 2 GB holding ~5 GB DB) — validate query work on warm/prod-like targets
- node-pg does **not** cancel Postgres when HTTP aborts — orphaned browse queries thrash cache (mitigated by statement_timeout + snapshot path)
- Employees lane still has a latent freeze pattern (discover 88 / process 0) — deferred separate ticket
- FLSP-548 AC#7 email parity guard intentionally descaled to on-demand script

## Status

Sync is **live** across three targets; parent FLSP-391 remains Testing while browse/order perf work continues (e.g. FLSP-783).
