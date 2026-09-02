---
title: ClearView Mobile / iPad Experience
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-30/
  - raw/fls-work/jira/2026-09-02/clearview-open-items.md
  - raw/fls-work/git/2026-09-02/AUDIT_REPORT.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
  - "[[work-log/2026-08-09-clearview-shop-rmf-sprint.md]]"
created: 2026-07-30
updated: 2026-09-02
confidence: high
tags: [clearview, mobile, ipad, responsive, furnitureland-south]
---

# ClearView Mobile / iPad Experience

Theme-sliced mobile/tablet work under Build Phase: back-navigation scroll, responsive chrome, camera scan on `/items`, render-budget fixes.

**Status:** **Done** (tracker as of 2026-09-02; was Post Prod Validation / camera scan open in July wiki)  
**Hub:** [[production-systems/inventory-lookup-clearview.md]]

## Work items

| Summary | Status |
|---------|--------|
| Restore `/items` scroll on back-navigation | **Done** (PR #74) |
| Tablet/iPad responsive pass | **Done** |
| Camera barcode scan on `/items` | **Done** (July "In Progress" superseded) |
| `/items` render-budget (grouped pagination overlap + lazy thumbs) | **Done** |

## Notable decisions

- **Back-nav scroll:** `history.scrollRestoration = "manual"`; Playwright `.click()` auto-scroll can invalidate scroll-restore tests.
- **Camera scan:** Scan applies barcode as `/items` filter (stay on list) — does not navigate to detail (avoids reintroducing back-nav friction).
- **Render budget:** Do not migrate result/detail images to `next/image` — plain `<img>` + Akeneo variants is deliberate.
