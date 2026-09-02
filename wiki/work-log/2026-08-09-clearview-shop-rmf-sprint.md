---
title: Work Period Summary — Aug–early Sep 2026 ClearView Shop/RMF
type: work-log
status: active
visibility: fls-internal
sources:
  - raw/fls-work/git/2026-09-02/AUDIT_REPORT.md
  - raw/fls-work/bitbucket/2026-09-02/inventory-lookup-delta.json
  - raw/fls-work/jira/2026-09-02/flsp-856-epic-tree.md
  - raw/fls-work/clearview-memory/2026-09-02/
related:
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[production-systems/clearview-notifications.md]]"
  - "[[production-systems/clearview-vra-handoff.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[overview.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [work-log, clearview, shop, rmf, august-2026, september-2026]
---

# Work Period Summary — Aug–early Sep 2026 ClearView Shop/RMF

Delta covering **2026-07-31 → 2026-09-02**. Prior: [[work-log/2026-07-30-four-week-lookback.md]].

**Sources:** git freeze (564 commits), Bitbucket (~104 merged PRs in window), Jira Parent-Link tree, Claude ClearView memories + Inventory-Lookup design specs frozen under `raw/fls-work/*/2026-09-02/`. Ticket keys scrubbed from this public vault.

## Executive snapshot

| Theme | Status | Wiki |
|-------|--------|------|
| PIE & Shop Replacement epic | In Progress | [[initiatives/pie-shop-replacement.md]] |
| Shop UI (tab/queue/detail) | Done | [[production-systems/clearview-shop-rmf-requests.md]] |
| NetSuite Shop Request record | Done (SB1 + prod) | same |
| Shop updates write-back | Post Prod Validation | same |
| RMF tab / nav | Testing | same |
| Notifications (subscribe email) | Done; sync-notify open | [[production-systems/clearview-notifications.md]] |
| VRA barcode handoff | Post Prod Validation | [[production-systems/clearview-vra-handoff.md]] |
| Mobile / iPad | **Done** (July open thread closed) | [[production-systems/clearview-mobile-ipad.md]] |
| Orders UX cleanup | Done | hub note |
| Post-demo refinements (8/31) | In Progress | initiative + Shop page |

## Volume

- ~**564** commits / ~**104** merged PRs on `inventory-lookup` in window
- Dominant theme: Shop/RMF (~233 commit hits); also orders UX, admin/RBAC, attachments, notifications, infra
- Stakeholder demos: Shop page **8/18**; Shop/RMF **8/31** (go-live month framing; training ~mid-September; Sept 30 absolute-latest for base completion)

## Architecture calls locked in this window

- Shop queue **reads live NetSuite** (not RDS) — [[decisions/clearview-shop-live-netsuite-read.md]]
- Transitional iSeries → NetSuite sync until BY/WMS create; closed comments → NSAW (~482K headers / ~1.99M logical comments)
- RMF = filter/nav on same record (not a second subsystem)
- Sub-location write **closed** as WMS/scan-owned
- Department Shop roles shipped behind `DEPARTMENT_SHOP_ROLES_ENABLED=false` until UAT flip
- Sync-notify code live; SMTP PLACEHOLDER/dual-block fixed 9/2 — sync-triggered email **confirmed working**

## Adjacent Build Phase carry-forward (same window)

- Orders UX cleanup (status tiles / mobile cards / abort-race) **Done**
- Mobile/iPad camera-scan story **Done**
- VRA handoff switched to **barcode** Suitelet intake (RA/SO-no-PO) — [[production-systems/clearview-vra-handoff.md]]

## Contradictions vs July 30 wiki

| July claim | Sep 2 |
|------------|-------|
| ClearView ≈ inventory + hosting | + Shop/RMF ops platform |
| Mobile camera scan still open | Mobile story **Done** |
| No Shop/RMF wiki coverage | Initiative + Tier A + ADRs + full memory/docs freeze |

## Open into September

- BY/WMS live create + DC Wrap closeout
- Flip department role flag when UAT ready
- RMF status wording / on-hold; resolution remap (external reply)
- VRA Suitelet prod URL flip
- NSAW archive-loader redeploy on task server
- ClearView Admin Users roster filed 2026-09-02 (76 users / 14 same-day / 9 `shop`) — [[production-systems/clearview-admin-users.md]]; PIE dual-run + Shop request volume still open
