---
title: RDS Delta Sync Watermarks (Drain-Safe Capping)
type: technique
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp547_txn_lane_drain.md
  - raw/fls-work/clearview-memory/2026-07-21/project_rds_delta_runner.md
  - raw/fls-work/clearview-memory/2026-07-21/project_delta_sync_build.md
related:
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[techniques/vmpn-serial-snapshot.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [clearview, delta-sync, watermark, postgres, suiteql, flsp-547, furnitureland-south]
---

# RDS Delta Sync Watermarks (Drain-Safe Capping)

How ClearView delta lanes advance `sync_state` watermarks under burst caps without permanently wedging — crystallized in [FLSP-547](https://furniturelandsouth.atlassian.net/browse/FLSP-547).

**Parent system:** [[production-systems/clearview-rds-delta-sync.md]]

## Problem pattern

Discover changed ids with `lastmodifieddate >= watermark - overlap`, then **cap** `maxPerCycle` for SuiteQL/time budgets. Naive v1 behavior:

1. No `ORDER BY` on discover
2. When capped: set `newWatermark = watermark` (freeze) and process only `ids.slice(0, maxPerCycle)`

Once the modified window exceeds the cap, the same first-N ids (SuiteQL default order) reprocess forever — watermark never advances. Observed on transactions: frozen at `2026-06-26 12:00:12` for ~6 days with `discovered ~41k capped=true` every cycle.

The freeze was meant as a data-loss guard; without ordering it became a permanent stall.

## Drain-safe rule

1. **`ORDER BY lastmodifieddate ASC`** on discover
2. Process oldest-N slice up to cap
3. Advance watermark to **max `lastmodifieddate` of the processed slice** even when capped
4. Keep a small server-side overlap (e.g. 2 min) for clock skew / late writes; derive seeds from `MAX(lastmodifieddate)`, never `SYSDATE - n`

Pure helper shape (`planTxnSlice`): sort → slice → watermark = max LMD of processed rows. Covered by `verify-txn-lane-drain.ts` in `verify:ci` (uncapped / capped / shuffled / empty / multi-cycle drain).

## Why ordering makes freeze safe

Every unprocessed row has `lmd >=` the slice max, so advancing to slice-max cannot skip older work. Self-heal on deploy: no migration — first cycles drain oldest 25k until discovered < cap.

## Residual edge

>25k rows sharing the **exact same one-second** `lastmodifieddate` could still stall — unrealistic for FLS volume; lever is raising `--max`.

## Sibling lanes

Same latent freeze pattern exists elsewhere if they ever exceed cap. Employees lane already shows discover-without-progress behavior for a shared LMD cluster — deferred separate ticket. Apply this drain helper when a lane hits the wedge.

## Related design notes

- Two-signal serials lane (inventorynumber + inventorynumberlocation) uses data-derived watermark + overlap
- Notes lane uses **id watermark** because LMD columns are not exposed — different mechanism, same "monotonic progress" requirement
