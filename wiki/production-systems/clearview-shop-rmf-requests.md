---
title: ClearView Shop / RMF Requests
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-09-02/flsp-856-story-descriptions.md
  - raw/fls-work/jira/2026-09-02/flsp-856-epic-tree.md
  - raw/fls-work/git/2026-09-02/inventory-lookup/adr-signals.json
  - raw/fls-work/git/2026-09-02/AUDIT_REPORT.md
  - raw/fls-work/clearview-memory/2026-09-02/
  - raw/fls-work/inventory-lookup-docs/2026-09-02/
  - repo:NetSuite/Inventory-Lookup
related:
  - "[[initiatives/pie-shop-replacement.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-notifications.md]]"
  - "[[production-systems/clearview-vra-handoff.md]]"
  - "[[decisions/clearview-shop-live-netsuite-read.md]]"
  - "[[decisions/clearview-shop-duplicate-guard.md]]"
  - "[[decisions/clearview-rmf-attachment-rendering.md]]"
  - "[[decisions/clearview-dev-role-admin-restrict.md]]"
  - "[[integrations/netsuite-suitetalk-jwt.md]]"
  - "[[work-log/2026-08-09-clearview-shop-rmf-sprint.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [clearview, shop, rmf, netsuite, custom-record, furnitureland-south]
---

# ClearView Shop / RMF Requests

ClearView's **Shop Request** surface replaces core PIE shop-tracking: queue + detail for active requests, NetSuite custom record as system of record, RMF as a filtered first-class nav on the **same** record type (not a separate subsystem), write-back for notes/status/resolution/attachments, and department-scoped view/create permissions.

**Initiative:** [[initiatives/pie-shop-replacement.md]]  
**Hub:** [[production-systems/inventory-lookup-clearview.md]]

⚠️ Epic and create/close automation are still **In Progress** — UI + custom record + most update paths shipped; live BY/WMS trigger and some post-demo items remain open. Department Shop roles ship behind a rollout flag (see Permissions).

## Problem

Shop teams needed a modern queue for items in shop workflow (damage, check-in, repair) with notes, photos, resolution, and cross-team visibility. PIE still carried follow-up behavior for some users. ClearView already had barcode identity and Entra RBAC — Shop/RMF extends that into ops.

## Architecture (what shipped)

| Piece | Choice |
|-------|--------|
| System of record | NetSuite `customrecordfls_shop_request` (+ status/type custom lists; **underscore-less** script ids locked at creation) |
| ClearView **read** path | **Live SuiteTalk / SuiteQL** — not RDS — [[decisions/clearview-shop-live-netsuite-read.md]] |
| Transitional write | iSeries PIE (`QS36F.DMGHDRPF` / comments) → NetSuite sync task until BY/WMS owns create |
| UI | `/shop` queue + detail; `/shop/rmf` as RMF filter + app-bar nav |
| Location model | Distinct **Shop** location — ~19 SHP-prefixed / Shop-legend codes (excludes SSHOP→Showroom, SHPPD→OTHER) |
| Duplicate guard | Block create when open request already exists for barcode — [[decisions/clearview-shop-duplicate-guard.md]] |
| Closed history | NSAW archive for ~1.99M closed comments; on-demand "Load historical comments" |
| Attachments | Upload + server-side render; HEIC/docs/BOL/email — [[decisions/clearview-rmf-attachment-rendering.md]] |
| Zendesk on detail | Priority/status + inline attachments; multi-ticket selector; Zendesk routes stay stricter gate |
| Permissions | Pilot `canAccessShop` + department **view** vs **create** — [[decisions/clearview-dev-role-admin-restrict.md]] |
| Subscriptions | Email on comment/attachment (+ sync-notify path) — [[production-systems/clearview-notifications.md]] |
| Relationships | Prior Shop/RMF for barcode + cases / RA / RI / Zendesk ticket history on detail |

## Scale (legacy → NetSuite)

Verified live from iSeries (Aug 2026), not estimates:

- **~482K** damage headers total; **~99.7% already closed**; only ~1.2K open at discovery time
- Comments: ~5.78M raw fixed-width rows → **~1.99M** logical comments after reassembly
- Approach: open-queue comments on live NetSuite record; closed history in **NSAW** (link-out / on-demand), not 2M NetSuite note rows
- SB1 sample backfill ~61K headers validated before prod promotion; dual-target sync (SB1 + prod) after prod record creation

## Capabilities by status (2026-09-02)

| Capability | Status |
|------------|--------|
| Shop nav, queue, filters, detail, empty/error states | Done |
| NetSuite Shop Request record (SB1 + prod) | Done |
| Create Request UI + barcode exists + duplicate open check | Done |
| Notes / status / resolution / dates write-back | Post Prod Validation |
| Resolution date server-stamped when Resolved | Done |
| Shop sub-location update | **Closed** — WMS/BY-owned; typed ClearView edit rejected (scan-vs-claim) |
| Admin/dev deletion path | Done (narrow; widen carefully) |
| Invisible `dev` role + Admin self-edit restrict | Done |
| RMF as top-level nav / filter on same record | Testing |
| Request relationships | Done |
| Department view/create role gating | Done — **rollout flag `DEPARTMENT_SHOP_ROLES_ENABLED` defaults false** until UAT flip |
| Driver title → `driver` + named beta pilots | Done (staging/prod) |
| Live BY/WMS create trigger | In Progress |
| Closeout on DC Wrap / leave-Shop | In Progress |
| NSAW archive loader + historical comment view | Done (resume/watermark fixes; task-server redeploy of loader still a ops thread) |

## RMF model

**RMF is not a second product.** Design locked: RMF = status/code filter + fields on the existing Shop Request record, with `/shop/rmf` route and app-bar placement. Assignee/date/status/follow-up for Check-In style work. Post-demo: status wording + on-hold still open with stakeholders; resolution remap (52→14) emailed to stakeholder — blocked on reply.

## Permissions (post-demo)

Two capability checks layered on the existing pilot gate (untouched):

- **View** — CS, design consultants (role 1042 + title match), purchasing, drivers, sales managers, plus pilot path
- **Create** — CS managers, purchasing managers, sales managers (plus pilot/admin)

Mutations (comment, attachment, status, subscribe) and **Zendesk** routes stay on stricter `canAccessShop` until a later widening (customer PII). Feature flag above is the master switch for department grants (~125 CS / ~48 Purchasing etc. on next sign-in when flipped).

Employee `title` column backfilled to RDS (migration + SuiteQL) so design-consultant matching works without freezing the employee delta lane.

## Sub-location / Blue Yonder (explicit non-ship)

Shop sub-location was scoped under write-back, then **closed** after WMS consultation:

- NetSuite `custitemnumber_wms_bin_location` is intended to mirror Blue Yonder; ClearView must not become a third writer
- Typed/dropdown location in a web form is a **claim**, not a verified scan — rejected for shop-floor truth
- Intra-Shop bay tracking granularity in BY still unresolved (Vince) — ClearView stays read-only for location until that lands

See frozen memory `project_wms_blue_yonder_integration.md` (local `raw/`).

## Notable ops lessons

- **NSAW `ewallet.pem`** exceeded SSM Advanced 8KB → Secrets Manager for that one value; other NSAW secrets stay SSM
- Archive loader must resume on **last_change_date**, not max barcode — barcode-forward scan missed closures for ~13 days (~450 headers)
- Scheduled `npx` without `--yes` hung forever on interactive prompt under Task Scheduler
- Dual-target shop sync (SB1 + prod); terraform/ECS secret population order still applies ([[production-systems/clearview-aws-hosting.md]])
- REST custom-record path is **type-direct** (`/record/v1/customrecordfls_shop_request`); grouped `customRecord/{scriptId}` 404/405s
- Custom-list fields need **internal ids**, not names; POST create returns **204** with id in `Location` header
- Date traps: legacy `DHODTE`/`DHRDTE` are unpadded M/D/YYYY (not YYYYMMDD); October misparsed until reconcile repaired thousands of rows
- Intermittent packet loss to Oracle Cloud NSAW (not firewall) complicated archive scheduling — root cause still open ⚠️

## Interview angles

- Custom NetSuite record + ClearView as ops UI with Entra RBAC tiers
- **Live SoT read for ops queues** vs RDS lag for catalog browse — same product, two freshness SLAs
- Same record, two product surfaces (Shop vs RMF) via filter/nav — avoid subsystem sprawl
- Archive to Oracle NSAW + on-demand historical load without bloating hot path
- Permission design: additive department roles + feature flag without breaking pilot gate
- Knowing when **not** to write location — WMS scan truth vs web form claim

## Open

See [[initiatives/pie-shop-replacement.md]]. ClearView user roster filed — [[production-systems/clearview-admin-users.md]] (9 explicit `shop` role). Shop/RMF request volume + PIE dual-run status still open.
