---
title: Inventory Lookup (ClearView) — Hosted NetSuite Inventory Intelligence
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp103_initiative_index.md
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp383_build_phase.md
  - raw/fls-work/clearview-memory/2026-07-21/project_inventory_lookup.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp403_aws_hosting.md
  - raw/fls-work/clearview-memory/2026-07-21/project_shared_rds_dev_db.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp508_approach_reporting.md
  - raw/fls-work/jira/2026-07-21/AUDIT_REPORT.md
  - repo:NetSuite/Inventory-Lookup
related:
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/pilot-database-migration.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[integrations/netsuite-suitetalk-jwt.md]]"
  - "[[techniques/vmpn-serial-snapshot.md]]"
  - "[[techniques/rds-delta-sync-watermarks.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
  - "[[decisions/clearview-location-movement-deferred.md]]"
  - "[[decisions/clearview-flsp384-umbrella.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
  - "[[production-systems/clearview-public-alb-waf.md]]"
  - "[[production-systems/clearview-clarity-telemetry.md]]"
  - "[[production-systems/clearview-ops-health.md]]"
  - "[[production-systems/clearview-admin-users.md]]"
  - "[[production-systems/clearview-mobile-ipad.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
  - "[[production-systems/sofascope.md]]"
  - "[[work-log/2026-05-period-summary.md]]"
created: 2026-05-20
updated: 2026-07-30
confidence: high
tags: [netsuite, next.js, suiteql, barcode, inventory, clearview, furnitureland-south, production, crm, aws, entra, rds]
---

# Inventory Lookup (ClearView) — Hosted NetSuite Inventory Intelligence

**ClearView** is Furnitureland South's modern Inventory Lookup product for Sales, Merchandising, and Operations: barcode scan, inventory browse, orders lookup, item history/timeline, and Approach-style export — replacing and extending the NetSuite **Review All Barcodes** suitelet.

**Strategic framing:** ClearView is the base groundwork for a serial-level CRM layer tracked through FLS's NetSuite ERP — every serial number's full lifecycle (receipt, sale, transfer, return, service activity) is a customer/product touchpoint, not just an inventory record.

## Scale & infrastructure

- **Catalogue:** ~1.3 million tracked serials across 200,000+ distinct products
- **Related records:** transactions, sales orders, returns, and other serial-tied activity queryable from a single lookup
- **Sync:** NetSuite → AWS RDS (Postgres) multi-lane delta sync (prod ~15 min cadence) — reads at volume hit RDS rather than SuiteQL; see [[production-systems/clearview-rds-delta-sync.md]]
- **Hosting:** ECS/Fargate + **internal and public** ALBs (staging + prod); public path WAF-protected — [[production-systems/clearview-aws-hosting.md]] · [[production-systems/clearview-public-alb-waf.md]]
- **Auth:** Microsoft Entra ID (Azure AD) SSO — see [[integrations/clearview-entra-sso.md]]

**Repo:** `CleanDevEnvironment/NetSuite/Inventory-Lookup/`

Parent initiative: [[initiatives/flsp-103-inventory-lookup.md]]. Historical May-2026 framing: [[work-log/2026-05-period-summary.md]] — **superseded for ClearView status by this page** (2026-07-21 rewrite).

## Contradiction callout

| Claim | Source | Status as of 2026-07-21 |
|-------|--------|-------------------------|
| FLSP-159 epic **Testing** | May 2026 wiki (`inventory-lookup-clearview.md`) | **Contradiction** — Jira status is **Post Prod Validation** |
| ClearView = SuiteTalk barcode tool + optional windowed pilot DB | May 2026 wiki | **Superseded** — hosted ECS/Fargate + Entra SSO + shared Postgres RDS (~5GB full history) + delta sync under FLSP-383 |

Do not use the May page or period summary as current ClearView status.

## Purpose

Floor and back-office staff need fast, accurate inventory intelligence while a customer is present: scan a barcode or browse filters, see item/pricing/availability context, follow the serial's movement story, look up related orders, and export filtered result sets (Approach successor) with **role-gated pricing**.

## Initiative

Under [[initiatives/flsp-103-inventory-lookup.md]] (Initiative **In Progress**):

| Epic | Name | Status (2026-07-21) |
|------|------|---------------------|
| [FLSP-104](https://furniturelandsouth.atlassian.net/browse/FLSP-104) | Discovery and Requirements Gathering | **Done** |
| [FLSP-167](https://furniturelandsouth.atlassian.net/browse/FLSP-167) | Design Phase | **Done** |
| [FLSP-159](https://furniturelandsouth.atlassian.net/browse/FLSP-159) | Review All Barcodes Suitelet | **Post Prod Validation** |
| [FLSP-383](https://furniturelandsouth.atlassian.net/browse/FLSP-383) | Build Phase | **In Progress** |

FLSP-159 is the early suitelet / pricing groundwork; the hosted product lives under FLSP-383. [FLSP-384](https://furniturelandsouth.atlassian.net/browse/FLSP-384) ("Search and lookup core") is **Done** in live Jira (2026-07-02). Earlier keep-open umbrella instruction is superseded — see [[decisions/clearview-flsp384-umbrella.md]].

## Stack

| Layer | Choice |
|-------|--------|
| App | Next.js App Router, React, TypeScript, Tailwind (FLS design tokens) |
| NetSuite live | SuiteTalk REST + SuiteQL, OAuth 2.0 JWT (PS256); optional SuiteAnalytics ODBC for notes when JWT role is insufficient — [[integrations/netsuite-suitetalk-jwt.md]] |
| NL timeline parse | NVIDIA NIM (Llama 3.3 70B) — graceful degradation if key absent |
| Read plane | **Postgres RDS (~5GB, full ~23-yr history)** — not a date-windowed pilot subset; see [[production-systems/pilot-database-migration.md]] status note · [[production-systems/clearview-rds-delta-sync.md]] |
| Auth | Microsoft Entra SSO via Auth.js (NextAuth v5); role-gated pricing / export columns — [[integrations/clearview-entra-sso.md]] |
| Hosting | ECS/Fargate behind shared ALB; staging + prod; internal DNS live — [[production-systems/clearview-aws-hosting.md]] |
| CI/CD | Bitbucket (`verify:ci` gate; OIDC deploy; auto staging, manual prod promote) |

## Surfaces

| Route | Purpose |
|-------|---------|
| `/` | ClearView home — camera/manual barcode entry, recent searches |
| `/detail/[barcode]` | Product detail — activity feed, timeline, case notes, role-gated pricing |
| `/items` | All Items — inventory search grid (flat or grouped-by-VMPN); export CSV/XLSX |
| `/classic` | Legacy UI — previous gradient lookup + drawers |
| Orders routes | Orders lookup (FLSP-389 Done) — separate from inventory search |

Images: three-tier Akeneo → SofaScope CDN → NetSuite File Cabinet (see [[production-systems/sofascope.md]] for the CDN path).

## Data plane

**Two paths (high level):**

1. **NetSuite live** — SuiteTalk JWT SuiteQL for lookup/timeline when configured; ODBC fallback for support-case notes when role permissions differ.
2. **RDS read path** — app serves inventory browse/detail/orders from shared Postgres; keep-fresh via multi-lane **delta sync** (transactions, customers, notes, cases, returns, serials) on an on-prem task-server cadence. Full-scale parity completed 2026-06-22 (~5GB); sync grows the DB incrementally thereafter.

Deep subsystem pages: [[production-systems/clearview-aws-hosting.md]], [[production-systems/clearview-rds-delta-sync.md]], [[techniques/rds-delta-sync-watermarks.md]], [[techniques/vmpn-serial-snapshot.md]], [[integrations/fls-aws-topology.md]], [[integrations/netsuite-suitetalk-jwt.md]].

## Auth

- **Entra SSO** for hosted staging/prod (FLSP-414 Done); login page shipped — [[integrations/clearview-entra-sso.md]].
- **Role-gated pricing** on detail and export paths — restricted roles must not see wholesale/cost/MSRP columns (flat and grouped export share the same gate after FLSP-508 fix).
- Auth.js v5 note: the wrapped `auth((req) => …)` middleware form can discard the `authorized` callback — gate must check `req.auth` explicitly (regression fixed 2026-07-16). See [[integrations/clearview-entra-sso.md]] and [[decisions/authjs-v5-authorized-callback.md]].

## Ops

| Area | Status (2026-07-30) |
|------|---------------------|
| CI quality gate | `verify:ci` (PGlite-safe) on PRs + main — Done |
| AWS hosting | **Post Prod Validation** — internal + public ALBs; Cloudflare CNAMEs live — [[production-systems/clearview-aws-hosting.md]] · [[production-systems/clearview-public-alb-waf.md]] |
| Sync runner | Task-server multi-target delta; ops health parity PASS — [[production-systems/clearview-rds-delta-sync.md]] · [[production-systems/clearview-ops-health.md]] |
| Cost posture | Ops health ~**$159/mo** steady-state (under prior ~$201–216 expectation) |
| UAT telemetry | Microsoft Clarity on prod — [[production-systems/clearview-clarity-telemetry.md]] |
| Admin / RBAC | Users override page shipped — [[production-systems/clearview-admin-users.md]] |

## Approach reporting

[FLSP-508](https://furniturelandsouth.atlassian.net/browse/FLSP-508) **Done** (2026-07-21, PR #58): CSV/XLSX export (flat + grouped-by-VMPN), column picker, **shared pricing-visibility gate**, tests in `verify:ci`. Deep page: [[production-systems/approach-reporting.md]]. ADR: [[decisions/clearview-approach-export-scope.md]].

**Explicitly deferred:** PDF export; multi-pivot Approach report templates (grand totals, DC-stock-by-manufacturer, location exception reports). Revisit from that deferred list — do not re-scope from scratch.

## Open work (2026-07-30)

| Item | Status | Notes |
|------|--------|-------|
| Mobile/iPad | Post Prod Validation | [[production-systems/clearview-mobile-ipad.md]]; camera scan still In Progress |
| Data Sync and Performance | Post Prod Validation | |
| AWS Hosting | Post Prod Validation | Public ALB live |
| Ops health | Testing | Parent open; sub-tasks Done — [[production-systems/clearview-ops-health.md]] |
| Chrome extension front-page break | In Progress | Bug (Jaylon) |
| Akeneo images 503 + missing sign-in video | In Progress | Bug (SSM) |
| ECS Auto Scaling | In Progress | |
| Post-launch hardening | In Progress | |
| Optimize order-list query | In Progress | |

Late-July lookback: [[work-log/2026-07-30-four-week-lookback.md]]. Ticket keys live in private tracker / local `raw/fls-work/` (not this public vault).

## Interview angles

- **Performance guards** — browse APIs require filters before unbounded SuiteQL/RDS load; grouped browse uses matview snapshot + statement timeouts for concurrent capacity.
- **Hybrid NetSuite + RDS** — live SuiteTalk for some paths; full-history Postgres read plane kept fresh by multi-lane delta sync.
- **RBAC export gating** — pricing columns stripped for restricted roles on both flat and grouped Excel/CSV (Approach successor).
- **Public + Entra** — internet-reachable inventory app with WAF + SSO, not VPN-only.
- **Stakeholder loop** — discovery → design → Build Phase demos → Jira feedback → ship; FLSP-384 closed Done in Jira after umbrella period.

## Deep pages

### Production systems
- [[production-systems/clearview-aws-hosting.md]]
- [[production-systems/clearview-public-alb-waf.md]]
- [[production-systems/clearview-rds-delta-sync.md]]
- [[production-systems/approach-reporting.md]]
- [[production-systems/clearview-clarity-telemetry.md]]
- [[production-systems/clearview-ops-health.md]]
- [[production-systems/clearview-admin-users.md]]
- [[production-systems/clearview-mobile-ipad.md]]

### Integrations
- [[integrations/clearview-entra-sso.md]]
- [[integrations/fls-aws-topology.md]]
- [[integrations/netsuite-suitetalk-jwt.md]]

### Techniques
- [[techniques/vmpn-serial-snapshot.md]]
- [[techniques/rds-delta-sync-watermarks.md]]

### ADRs
- [[decisions/clearview-approach-export-scope.md]]
- [[decisions/clearview-location-movement-deferred.md]]
- [[decisions/clearview-flsp384-umbrella.md]]
- [[decisions/authjs-v5-authorized-callback.md]]