---
title: Inventory Lookup (ClearView) — NetSuite Barcode Intelligence
type: production-system
status: active
visibility: fls-internal
sources: [jira:FLSP-159, jira:FLSP-221, repo:NetSuite/Inventory-Lookup]
related: [[production-systems/pilot-database-migration.md]], [[integrations/netsuite-zendesk-customer-sync.md]], [[work-log/2026-05-period-summary.md]]
created: 2026-05-20
updated: 2026-07-11
confidence: high
tags: [netsuite, next.js, suiteql, barcode, inventory, clearview, furnitureland-south, production, crm, aws, entra-id]
---

# Inventory Lookup (ClearView) — NetSuite Barcode Intelligence

Modern replacement and extension of the NetSuite **Review All Barcodes** suitelet. Scan or enter a barcode to retrieve full inventory context: item details, receipt history, sales orders, return inventory, RtnAuth lines, support-case notes, optional damage/pricing fields, and a transaction timeline.

**Strategic framing:** ClearView is the base groundwork for a serial-level CRM layer tracked through FLS's NetSuite ERP — every serial number's full lifecycle (receipt, sale, transfer, return, service activity) is a customer/product touchpoint, not just an inventory record.

## Scale & infrastructure

- **Catalogue:** ~1.3 million tracked serials across 200,000+ distinct products
- **Related records:** transactions, sales orders, returns, and all other activity tied to a given serial are captured and made queryable from a single lookup
- **Sync:** NetSuite → pilot store sync runs every 15 minutes, trading strict real-time consistency for query speed and lower NetSuite/SuiteQL load — reads at these volumes hit the synced store rather than SuiteQL directly (see [[production-systems/pilot-database-migration.md]])
- **Hosting:** AWS
- **Auth:** Microsoft Entra ID (Azure AD) gating in front of the app
- **Network exposure:** internal-network only — never exposed to the public internet

**Jira:** [FLSP-159 Review All Barcodes Suitelet](https://furniturelandsouth.atlassian.net/browse/FLSP-159) (Epic, Testing) · [FLSP-221 Sales feedback](https://furniturelandsouth.atlassian.net/browse/FLSP-221)

**Repo:** `CleanDevEnvironment/NetSuite/Inventory-Lookup/`

## Stack

- **Frontend:** Next.js App Router, React, TypeScript, Tailwind CSS
- **State:** Zustand + localStorage (search history, groups)
- **Backend:** SuiteTalk REST + SuiteQL (`lib/netsuite.ts`), OAuth 2.0 JWT (PS256)
- **Optional reads:** SuiteAnalytics ODBC (`lib/netsuite-odbc.ts`) for case notes when JWT role is insufficient
- **NL parsing:** NVIDIA NIM (Llama 3.3 70B) for timeline filter parsing — graceful degradation if key absent
- **Pilot DB:** Postgres migration subsystem (see [[production-systems/pilot-database-migration.md]])

## User experiences

| Route | Name | Purpose |
|-------|------|---------|
| `/` | ClearView home | Camera/manual barcode entry, recent searches |
| `/detail/[barcode]` | Product detail | Unified problem/activity feed, timeline, case notes |
| `/items` | All Items | Inventory search grid (flat or grouped-by-VMPN) |
| `/classic` | Legacy UI | Previous gradient lookup + drawers |

## API surface

| Endpoint | Purpose |
|----------|---------|
| `GET /api/lookup?barcode=` | Full barcode context (item, receipts, SOs, RI, RtnAuth, images, derived Zendesk case IDs) |
| `GET /api/inventory-search` | All-items search (powers `/items`) |
| `GET /api/inventory-browse` | Suitelet-parity browse — **requires ≥1 filter** before row load (performance guard) |
| `GET /api/case-notes?caseId=` | Support case notes (SuiteQL + optional ODBC) |
| `GET /api/ns-file?fileId=` | Stream File Cabinet bytes for same-origin thumbnails |
| `POST /api/timeline` | Filtered transaction timeline |
| `POST /api/timeline/parse` | Natural language → timeline filters |

## NetSuite integration pattern

Auth and SuiteQL plumbing follow the **`ja-utility-shed`** utility pattern:
- JWT signing + token exchange
- In-process access token cache
- SQL literal escaping + identifier validation

Key query builders live in `lib/queries.ts`. Optional env-gated columns for pricing and damage fields on `inventorynumber`.

## May 2026 sales feedback (FLSP-221)

Carmen Wilkins (sales team) submitted five requests; implemented in testing, validated, rolling to production:

1. **Available filter** — Available / Not Available dropdown (distinct from "Is On Hand")
2. **Tag Type deduplication** — Normalize case-variant duplicates (`fso` / `FSo` / `FS0`) in filter options
3. Additional UX/filter items documented in Jira comment thread

## Roadmap (from repo README)

1. Confirm JWT role can read `itemimage` + `file` joins; improve empty-state UX for missing Web Store images
2. Full suitelet parity on `/items` — filters, primary image column, grouped performance, role-gated SuiteQL gaps

## Related child tickets

- [FLSP-208](https://furniturelandsouth.atlassian.net/browse/FLSP-208) Refine search and results features
- [FLSP-209](https://furniturelandsouth.atlassian.net/browse/FLSP-209) Refine Item Details
- [FLSP-207](https://furniturelandsouth.atlassian.net/browse/FLSP-207) Capture Feedback from Walkthroughs

## Interview angles

- **Performance guard pattern:** `/api/inventory-browse` requires filters before loading rows — mirrors suitelet behavior to prevent unbounded SuiteQL
- **Hybrid data access:** JWT SuiteQL for primary path, ODBC fallback for notes when role permissions differ
- **Stakeholder-driven iteration:** Structured feedback → Jira → implement → test → production rollout
