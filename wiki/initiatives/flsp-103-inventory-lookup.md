---
title: FLSP-103 — Inventory Lookup Tool Initiative
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp103_initiative_index.md
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp104_discovery_epic.md
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp167_design_epic.md
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp159_barcodes_suitelet_epic.md
  - raw/fls-work/jira/2026-07-21/flsp-103/project_flsp383_build_phase.md
  - raw/fls-work/jira/2026-07-21/AUDIT_REPORT.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[production-systems/clearview-notifications.md]]"
  - "[[production-systems/clearview-vra-handoff.md]]"
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
  - "[[decisions/clearview-shop-live-netsuite-read.md]]"
  - "[[work-log/2026-05-period-summary.md]]"
  - "[[work-log/2026-08-09-clearview-shop-rmf-sprint.md]]"
created: 2026-07-21
updated: 2026-09-02
confidence: high
tags: [initiative, jira-index, clearview, inventory-lookup, furnitureland-south, fls-internal]
---

# FLSP-103 — Inventory Lookup Tool Initiative

[FLSP-103](https://furniturelandsouth.atlassian.net/browse/FLSP-103) is the top-level **Initiative** (hierarchy above Epic) for Furnitureland South's internal Inventory Lookup Tool (ClearView). Goal: faster, more accurate inventory access for Sales, Merchandising, and Operations — covering discovery, design, build, validation, and rollout.

**Status:** In Progress (as of 2026-09-02).

**Major new epic (standalone wiki page):** [[initiatives/pie-shop-replacement.md]] — PIE & Shop Replacement (Shop/RMF). Original four epics remain indexed below on this fat page.
Deep product synthesis lives at [[production-systems/inventory-lookup-clearview.md]] (Tier A hub; rewrite in Task 2). This page is Tier B navigation only.

## Gotcha — Initiative Name rollup

The Jira **"Initiative Name" rollup** custom field (automation-backed) does **not** reliably backfill onto every child issue. It missed several bugs and older sub-tasks (e.g. FLSP-109, FLSP-547–549, FLSP-565, FLSP-647, FLSP-781, FLSP-784).

**True tree:** `"Parent Link" = FLSP-103` for epics, then `parent in (...)` recursively for stories and sub-tasks. Do not trust the rollup field alone.

## Four epics (inline index)

Totals as of 2026-07-21: **4 epics**, **30 stories/bugs**, **90 sub-tasks**.

### FLSP-104 — Discovery and Requirements Gathering

| | |
|---|---|
| **Key** | [FLSP-104](https://furniturelandsouth.atlassian.net/browse/FLSP-104) |
| **Status** | Done |
| **Assignee** | Jaylon Norris (default); Cameron on noted items |

- **FLSP-105** Done — Identify target users and primary use cases
  - FLSP-106 Done — Meet with Sales stakeholders
  - FLSP-107 Done — Meet with Merchandising stakeholders
  - FLSP-118 Done (Cameron) — PIE Meeting w Danny
  - FLSP-130 Done — PIE Meeting w/ CS, Merchandising, and Operations
  - FLSP-135 Done — Check-In On-Site Visit
  - FLSP-136 Done (Cameron) — Check-In Meeting w Danny
  - FLSP-137 Done (Cameron) — Approach Meeting w Kirk (origin of Approach/legacy-report discovery)
  - FLSP-158 Done (Cameron) — Service Pro Meeting w Danny
  - FLSP-161 Done — Service Pro Discovery w/ Stakeholders
- **FLSP-108** Done — Document discovery outputs (current state, requirements, success criteria)
  - FLSP-109 Done — Document current-state inventory lookup and Legacy System Usages
  - FLSP-110 Done (Cameron) — Map inventory data flow and dependencies
  - FLSP-111 Done (Cameron) — Identify required data elements
  - FLSP-112 Done — Compile open questions, risks, and decisions needed
  - FLSP-113 Done — Confirm system access requirements
- **FLSP-114** Done — Discovery closeout, review and sign-off
  - FLSP-115 Done — Stakeholder review session and decisions capture
- **FLSP-116** Done — Tech Stack Discovery and Early Architecture Notes
  - FLSP-117 Done — Log cool ideas
  - FLSP-131 Done — Wireframe of Tool (early ClearView wireframe)

### FLSP-167 — Design Phase

| | |
|---|---|
| **Key** | [FLSP-167](https://furniturelandsouth.atlassian.net/browse/FLSP-167) |
| **Status** | Done |
| **Assignee** | Mixed Jaylon / Cameron |

- **FLSP-195** Done (Jaylon) — Inventory Search, Filters & Results Design
  - FLSP-199–202, FLSP-205–206 Done — search inputs, filters, results layout, drill-in, photos
  - FLSP-203 Done (Cameron) — Performance Guardrails
- **FLSP-196** Done (Jaylon) — Item Detail, History & Photos (Progressive Disclosure)
  - FLSP-204, FLSP-225–227 Done — default detail, history/notes, photo UX, progressive disclosure
- **FLSP-197** Done (Cameron) — Technical Guardrails, Repo Structure & Environment Discipline
  - FLSP-210–212, FLSP-228, FLSP-232 Done — repo principles, env separation, v1 stack, pipeline, testing DB
- **FLSP-198** Post Prod Validation (Cameron) — Visual Design & Lightweight Prototype Refinement
  - FLSP-207–209, FLSP-258–260 Done — walkthrough feedback, search/results/detail refinements, demo readiness

### FLSP-159 — Review All Barcodes Suitelet

| | |
|---|---|
| **Key** | [FLSP-159](https://furniturelandsouth.atlassian.net/browse/FLSP-159) |
| **Status** | Post Prod Validation |
| **Assignee** | Cameron (all items) |

Smallest epic; early suitelet / pricing groundwork that preceded the hosted ClearView product.

- **FLSP-221** Done — Waiting for feedback
- **FLSP-222** Done — Explore Role Based Pricing Views
- **FLSP-272** Bug, Done — Item Commission Code Sourcing
  - FLSP-273 Done — Production Validation

### FLSP-383 — Build Phase

| | |
|---|---|
| **Key** | [FLSP-383](https://furniturelandsouth.atlassian.net/browse/FLSP-383) |
| **Status** | In Progress |
| **Assignee** | Jaylon (epic); Cameron owns most build stories |

Active production-build epic. Almost everything Done; open remainder listed below.

**FLSP-384 note:** [FLSP-384](https://furniturelandsouth.atlassian.net/browse/FLSP-384) is **Done** in live Jira (updated 2026-07-02). Earlier catch-up text said keep **In Progress** as an umbrella — that instruction is superseded. Historical rationale: [[decisions/clearview-flsp384-umbrella.md]].

- **FLSP-384** Done (Cameron) — Search and lookup core
  - FLSP-393 Done (Jaylon) — Research synonym and normalization handling
- **FLSP-385** Done (Jaylon) — Inventory Filters and Controls
  - FLSP-394–396 Done — expanded filters, multi-select, sellable/available toggle
- **FLSP-386** Done (Cameron) — Inventory Results Display (Scan-First UX)
  - FLSP-397–398, FLSP-416, FLSP-419 Done — result cards, client sort, Excel/CSV export, On Order status
- **FLSP-387** Done (Cameron) — Item Detail Experience (Barcode View)
  - FLSP-399–400, FLSP-402, FLSP-417–418, FLSP-533–534 Done — pricing visibility, Internal ID, txn status, Eazy Tags, SO-only, FSO/SPO labels, VMPN count bubble
- **FLSP-388** Done (Cameron) — Item History/Activity
  - FLSP-401 Done — Show location movement clearly *(building-level version deferred; not what shipped)*
- **FLSP-389** Done (Jaylon) — Orders Lookup (Separate from Inventory Search)
  - FLSP-420–421, FLSP-485–487, FLSP-525, FLSP-532 (Cameron), FLSP-648 Done — order page, filters, financials, location, bugs, item type
- **FLSP-390** Post Prod Validation (Cameron) — Mobile/iPad — [[production-systems/clearview-mobile-ipad.md]] (camera scan still In Progress)
- **FLSP-391** Post Prod Validation (Cameron) — Data Sync and Performance
  - FLSP-446, FLSP-511, FLSP-551, FLSP-585, FLSP-587–588, FLSP-646 Done — shared RDS, delta runner, browse query, back-nav, cached results, concurrent capacity, per-serial snapshot
  - FLSP-783 In Progress — Optimize order-list query
- **FLSP-403** Post Prod Validation (Cameron) — AWS Hosting — [[production-systems/clearview-aws-hosting.md]] · [[production-systems/clearview-public-alb-waf.md]]
  - FLSP-405–411, FLSP-413 Done — ALB, ECS/Fargate, cost, RDS, connectivity, CI/CD, logging, env strategy
  - FLSP-412 In Progress — Configure Auto Scaling for ECS
  - FLSP-728 In Progress — Post-launch hardening follow-ups
- **FLSP-414** Done (Cameron) — Security / SSO (Entra)
  - FLSP-490–496 Done — Entra auth, staging, roles, session, employee delta, API/UI gating, RBAC
  - FLSP-544 Done (Jaylon) — Login Page
- **FLSP-474** Done (Cameron) — Bitbucket Pipeline (CI quality gate)
- **FLSP-508** Done (Cameron) — Reporting aka Approach
- **FLSP-547** Bug, Done (Cameron) — Delta runner transactions lane wedged
- **FLSP-548** Bug, Done (Cameron) — RDS vs NetSuite transaction parity gap
- **FLSP-549** Bug, Done (Cameron) — Item History NetSuite deep links open SB1
- **FLSP-565** Bug, In Progress (Jaylon) — Chrome extension breaking front page
- **FLSP-647** Bug, Done (Jaylon) — Orders Page non-inventory lines inflate counts
- **FLSP-781** Bug, Done (Cameron) — clearview-staging crash-loop (RDS password / SSM drift)
- **FLSP-784** Bug, In Progress (Cameron) — Hosted ClearView: Akeneo images 503 + missing sign-in video

## Open items as of 2026-09-02

Ticket keys omitted from this public vault (join in private tracker / local `raw/fls-work/`).

| Item | Status | Notes |
|------|--------|-------|
| PIE & Shop Replacement | In Progress | Standalone — [[initiatives/pie-shop-replacement.md]] |
| Shop create/close automation | In Progress | BY/WMS trigger + closeout |
| RMF tab | Testing | [[production-systems/clearview-shop-rmf-requests.md]] |
| Shop notifications expansion | In Progress | [[production-systems/clearview-notifications.md]] |
| Post-demo roles / access testing | In Progress | View/create permissions Done |
| VRA handoff | Post Prod Validation | [[production-systems/clearview-vra-handoff.md]] |
| Data Sync and Performance | Post Prod Validation | |
| AWS Hosting | Post Prod Validation | Public ALB live |
| Ops health | Testing | Parent — [[production-systems/clearview-ops-health.md]] |
| Chrome extension front-page break | In Progress | Bug (Jaylon) |
| Akeneo 503 + sign-in video | In Progress | Bug (Cameron) |
| ECS Auto Scaling | In Progress | Sub-task |
| Post-launch hardening | In Progress | Sub-task |

Mobile/iPad: **Done** — [[production-systems/clearview-mobile-ipad.md]].

## Cameron footprint

Assignee ClearView / FLSP-103 cluster: **~79 issues** at 2026-07-21 audit; Aug–Sep Shop/RMF added substantial volume (~564 commits on inventory-lookup). Full initiative tree also includes Jaylon Norris and other assignees — this page indexes the whole Parent-Link tree, not Cameron-only.

## Wiki topology

| Tier | Role | Page |
|------|------|------|
| **B** | Initiative navigation (this page) | `wiki/initiatives/flsp-103-inventory-lookup.md` |
| **B** | PIE & Shop Replacement | [[initiatives/pie-shop-replacement.md]] |
| **A** | Product hub | [[production-systems/inventory-lookup-clearview.md]] |
| **A** | Shop / RMF | [[production-systems/clearview-shop-rmf-requests.md]] |
| **A** | Notifications | [[production-systems/clearview-notifications.md]] |
| **A** | VRA handoff | [[production-systems/clearview-vra-handoff.md]] |
| **A** | AWS hosting | [[production-systems/clearview-aws-hosting.md]] |
| **A** | Public ALB + WAF | [[production-systems/clearview-public-alb-waf.md]] |
| **A** | RDS delta sync | [[production-systems/clearview-rds-delta-sync.md]] |
| **A** | Approach reporting | [[production-systems/approach-reporting.md]] |
| **A** | Clarity telemetry | [[production-systems/clearview-clarity-telemetry.md]] |
| **A** | Ops health | [[production-systems/clearview-ops-health.md]] |
| **A** | Admin users | [[production-systems/clearview-admin-users.md]] |
| **A** | Mobile / iPad | [[production-systems/clearview-mobile-ipad.md]] |
| **A** | Entra SSO | [[integrations/clearview-entra-sso.md]] |
| **A** | AWS topology | [[integrations/fls-aws-topology.md]] |
| **A** | SuiteTalk JWT | [[integrations/netsuite-suitetalk-jwt.md]] |
| **A** | Techniques | [[techniques/vmpn-serial-snapshot.md]] · [[techniques/rds-delta-sync-watermarks.md]] |
| **A** | ADRs | [[decisions/clearview-approach-export-scope.md]] · [[decisions/clearview-location-movement-deferred.md]] · [[decisions/clearview-flsp384-umbrella.md]] · [[decisions/authjs-v5-authorized-callback.md]] |
| **A** | Related | [[production-systems/pilot-database-migration.md]] |
| **C / log** | Period context | [[work-log/2026-05-period-summary.md]] |
