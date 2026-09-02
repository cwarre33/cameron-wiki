---
title: PIE & Shop Replacement
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-09-02/flsp-856-epic-tree.md
  - raw/fls-work/jira/2026-09-02/flsp-856-story-descriptions.md
  - raw/fls-work/git/2026-09-02/AUDIT_REPORT.md
  - raw/fls-work/clearview-memory/2026-09-02/project_shop_rmf_postdemo_followups_20260831.md
  - raw/fls-work/clearview-memory/2026-09-02/project_shop_page_meeting_20260818.md
  - raw/fls-work/clearview-memory/2026-09-02/MEMORY.md
related:
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[production-systems/clearview-notifications.md]]"
  - "[[production-systems/clearview-vra-handoff.md]]"
  - "[[decisions/clearview-shop-live-netsuite-read.md]]"
  - "[[work-log/2026-08-09-clearview-shop-rmf-sprint.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [initiative, clearview, shop, rmf, pie-replacement, furnitureland-south]
---

# PIE & Shop Replacement

Standalone initiative page for ClearView's **PIE replacement** workstream under the Inventory Lookup parent initiative ([[initiatives/flsp-103-inventory-lookup.md]]). Goal: shop request tracking, notes/comments, photos, and visibility for Service, Sales, Merchandising, Warehouse, and Shop — without forcing users back into legacy PIE for day-to-day shop ops.

**Status:** In Progress (as of 2026-09-02). **Do not claim epic Done.**

Deep system page: [[production-systems/clearview-shop-rmf-requests.md]].

## Why this exists

Legacy PIE was still the shop / follow-up surface for some teams. ClearView already owned barcode identity, item history, and Entra RBAC — this epic extends that into **Shop Request** and **RMF** workflows with NetSuite as system of record (live reads; transitional iSeries sync until Blue Yonder owns create — [[decisions/clearview-shop-live-netsuite-read.md]]).

Primary queue consumer historically framed as Jason Grubb's Shop team; broader department visibility expanding via feature-flagged roles.

## Timeline (stakeholder)

| Date | Event |
|------|-------|
| 2026-08-18 | Shop page meeting — usability, SHP location, RMF scope; **Sept 30** absolute-latest framing for base completion before training/comms |
| 2026-08-31 | Shop/RMF stakeholder demo + Cameron/Jaylon post-demo call — **final development month** before go-live; training tentatively **second week of September** |
| 2026-09-02 | Department role permissions merged + prod-promoted; rollout flag still off pending UAT |

**Adoption (ClearView overall, not Shop-only):** 76 Admin-listed users; 14 seen 2026-09-02; 9 with explicit `shop` role — [[production-systems/clearview-admin-users.md]]. Shop/RMF request volume still unknown. ⚠️ PIE dual-run vs fully replaced still needed from Cameron.

## Story index (compact, scrubbed)

| Theme | Status | Notes |
|-------|--------|-------|
| Workflow / data model / BY–WMS approach | In Progress | Collaborator-led definition; entry triggers & SoR decisions |
| Create/close from status/location | In Progress | NetSuite Shop Request Done; live BY/WMS trigger + DC Wrap closeout still open |
| Shop tab / queue / detail UI | Done | Filters (apply/enter), resolution dropdown, color count cards, click→request detail |
| Authorized updates from ClearView | Post Prod Validation | Notes, status, resolution, attachments write-back; sub-location closed as WMS |
| PIE notes migration + item comments | Done | Legacy notes → NetSuite serial notes; ClearView write-back |
| Notifications / lightweight tasks | In Progress | Subscribe + sync-change notify Done/live; parent story still open for task-lite decision |
| RMF tab | Testing | Same Shop Request record + filter/nav |
| Shop as distinct SHP location | Done | ~19 Shop codes; not grouped under DC |
| User menu / version footer | Done | Welcome + sign-out; drop hard-coded version footer |
| Post-demo refinements | In Progress | Attachments/relationships/subscribe UX/permissions Done; resolution remap + RMF status wording + access testing open |

## Post-demo backlog (8/31 → tracked)

| Item | State |
|------|-------|
| Resolution options remap (Choros / 52→14) | Mapping agreed; **blocked** on stakeholder reply |
| RMF status wording + on-hold | Open (stakeholder email loop) |
| Attachment type verification | Done — [[decisions/clearview-rmf-attachment-rendering.md]] |
| Resolution date auto-stamp | Done |
| Prior request + case/ticket relationships | Done |
| Department access testing (drivers, CS, …) | Joint; roles built, flag off |
| View vs create permissions by dept | Done (flagged) |
| Subscribe confirmation UX | Done |

## Topology

| Tier | Page |
|------|------|
| B (this page) | Initiative navigation |
| A | [[production-systems/clearview-shop-rmf-requests.md]] |
| A | [[production-systems/clearview-notifications.md]] |
| A | [[production-systems/clearview-vra-handoff.md]] (adjacent Development epic) |
| ADR | [[decisions/clearview-shop-live-netsuite-read.md]] · [[decisions/clearview-shop-duplicate-guard.md]] · [[decisions/clearview-rmf-attachment-rendering.md]] · [[decisions/clearview-dev-role-admin-restrict.md]] |

## Open entering September 2026

- Live create trigger from BY/WMS + closeout when item leaves Shop
- Flip `DEPARTMENT_SHOP_ROLES_ENABLED` when UAT ready
- RMF status wording / on-hold; resolution code remap (external reply)
- Workflow definition story still In Progress
- NSAW archive-loader redeploy on task server (resume fix already in main)

Ticket keys and full Parent-Link trees: `raw/fls-work/jira/2026-09-02/` (local only).
