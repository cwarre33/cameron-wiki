---
title: ClearView Mobile / iPad Experience
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-30/
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
created: 2026-07-30
updated: 2026-07-30
confidence: high
tags: [clearview, mobile, ipad, responsive, furnitureland-south]
---

# ClearView Mobile / iPad Experience

Theme-sliced mobile/tablet work under Build Phase: back-navigation scroll, responsive chrome, camera scan on `/items`, render-budget fixes.

**Status:** Post Prod Validation (as of 2026-07-24)  
**Hub:** [[production-systems/inventory-lookup-clearview.md]]

## Work items

| Summary | Status (late July) |
|---------|-------------------------|
| Restore `/items` scroll on back-navigation | **Done** (PR #74) |
| Tablet/iPad responsive pass | **Done** |
| Camera barcode scan on `/items` | **In Progress** |
| `/items` render-budget (grouped pagination overlap + lazy thumbs) | **Done** |

⚠️ Claude memory dated 2026-07-24 still listed tablet pass / render-budget as "not started"; live tracker shows them Done — trust tracker for closeout status.

## Notable decisions

- **Back-nav scroll:** `history.scrollRestoration = "manual"`; Playwright `.click()` auto-scroll can invalidate scroll-restore tests.
- **Camera scan:** Scan applies barcode as `/items` filter (stay on list) — does not navigate to detail (avoids reintroducing back-nav friction).
- **Render budget:** Do not migrate result/detail images to `next/image` — plain `<img>` + Akeneo variants is deliberate.
