---
title: ClearView Ops Health Check
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-30/
related:
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/clearview-public-alb-waf.md]]"
  - "[[techniques/rds-delta-sync-watermarks.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
created: 2026-07-30
updated: 2026-07-30
confidence: high
tags: [clearview, ops, cost, parity, delta-sync, furnitureland-south]
---

# ClearView Ops Health Check

Post-provision ops health across **parity**, **sync logs**, and **cost** after public ALB / hosting landed.

**Status:** Parent story Testing; sub-tasks Done as of 2026-07-29  
**Hub:** [[production-systems/inventory-lookup-clearview.md]]

## Results (2026-07-28)

| Focus | Outcome |
|-------|---------|
| NetSuite↔RDS parity (dev/staging/prod) | **PASS** all envs (headers/lines/serials above thresholds) |
| Task-server delta-sync logs | New `scripts/analyze-delta-sync-logs.ts` (PRs #82–84); dev/prod healthy |
| Cost allocation tags + revised estimate | **~$159/mo** steady-state — under prior ~$201–216 expectation |
| Staging stalled task + missing `inventory_facets_snapshot` | Filed from sync-log findings; **Done** 2026-07-29 |

## Quirks worth remembering

- Task server is **RDP-only** — log analysis tool must be run there; paste stdout back.
- Delta-sync `.bat` **never logs its own completion line** even on success (self-modifying script quirk) — judge health by cadence gaps, not missing "done" lines.

## Cost snapshot

Isolated ClearView from shared-account noise: RDS gp3/`db.t4g.*` usage types + computed ECS/ALB/WAF. Tags `project`/`env`/`managed-by` activated 2026-07-28 for future CE filtering.
