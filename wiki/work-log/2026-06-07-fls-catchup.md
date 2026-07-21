---
title: Work Period Summary — May–July 2026 FLS Catch-Up
type: work-log
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/AUDIT_REPORT.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/jira/2026-07-21/cameron-reporter-catalog.md
related:
  - "[[work-log/2026-05-period-summary.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[initiatives/zendesk-automation-platform.md]]"
  - "[[initiatives/sellsmart-program.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[production-systems/crr-round-robin.md]]"
  - "[[production-systems/zendesk-call-transcripts.md]]"
  - "[[production-systems/zendesk-shared-views.md]]"
  - "[[production-systems/zendesk-ticket-calendar.md]]"
  - "[[production-systems/digital-to-store-copilot.md]]"
  - "[[production-systems/dedicated-agent-assignment.md]]"
  - "[[production-systems/sellsmart-copilot.md]]"
  - "[[production-systems/sofascope.md]]"
  - "[[production-systems/zendesk-returns-reporting.md]]"
  - "[[production-systems/pilot-database-migration.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[integrations/fls-aws-topology.md]]"
  - "[[integrations/netsuite-suitetalk-jwt.md]]"
  - "[[integrations/netsuite-zendesk-customer-sync.md]]"
  - "[[integrations/sellsmart-netsuite-rest-tool.md]]"
  - "[[techniques/vmpn-serial-snapshot.md]]"
  - "[[techniques/rds-delta-sync-watermarks.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
  - "[[decisions/clearview-location-movement-deferred.md]]"
  - "[[decisions/clearview-flsp384-umbrella.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
  - "[[open-questions/zendesk-oauth-refresh-2026-10.md]]"
  - "[[methodology/neutral-history-framing.md]]"
  - "[[methodology/verify-against-source-docs.md]]"
  - "[[interview-prep/system-design-clearview.md]]"
  - "[[interview-prep/behavioral-fls-delivery.md]]"
  - "[[overview.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [work-log, fls, jira, clearview, zendesk, sellsmart, sofascope, may-july-2026]
---

# Work Period Summary — May–July 2026 FLS Catch-Up

Catch-up ingest covering **2026-05-21 → 2026-07-21**. Prior period: [[work-log/2026-05-period-summary.md]] (May 1–20). This page is the **navigation synthesis** for the July wiki rebuild (Tasks 1–8); deep status lives on linked hubs — do not treat the May summary as current ClearView / Zendesk status.

**Audit freeze:** `raw/fls-work/jira/2026-07-21/AUDIT_REPORT.md` · `cluster-map.md` · assignee catalog (333) / reporter catalog (206).

## Executive snapshot

| Cluster | Assignee issues | Done-ish / open-ish | Wiki tier | Hub |
|---------|----------------:|--------------------:|-----------|-----|
| ClearView / FLSP-103 | 79 | 73 / 6 | A + B | [[initiatives/flsp-103-inventory-lookup.md]] · [[production-systems/inventory-lookup-clearview.md]] |
| Zendesk automation | 108 | 106 / 2 | A + B | [[initiatives/zendesk-automation-platform.md]] |
| SofaScope / FLSI visual search | 93 | 90 / 3 | A | [[production-systems/sofascope.md]] |
| SellSmart / Copilot / DC Discovery | 42 | 33 / 9 | A + B | [[initiatives/sellsmart-program.md]] |
| Digital-to-Store / FLSP-247 | 6 | 4 / 2 | A + B | [[production-systems/digital-to-store-copilot.md]] |
| Transcripts / call automation | 2 | 2 / 0 | A (under Zendesk) | [[production-systems/zendesk-call-transcripts.md]] |
| ITT / service desk | 3 | 3 / 0 | C | catalog rows below |
| FLSM maintenance (standalone) | 0 | — | absorbed | SellSmart + Zendesk + [[open-questions/zendesk-oauth-refresh-2026-10.md]] |

**Portfolio totals (assignee):** 333 issues — FLSI 221 · FLSP 101 · FLSM 8 · ITT 3. Status category: Done 313 · In Progress 13 · To Do 7.

## What changed vs May 2026

| May claim | July 2026 reality |
|-----------|-------------------|
| ClearView ≈ SuiteTalk barcode tool + optional windowed pilot DB | Hosted product: ECS/Fargate + Entra SSO + shared RDS (~5GB full history) + multi-lane delta sync under FLSP-383 |
| FLSP-159 **Testing** | FLSP-159 **Post Prod Validation**; Build Phase (FLSP-383) **In Progress** |
| Dedicated agent FLSP-163 **Testing** | FLSP-163 **Done**; post-launch FLSI-2965 still Ready for Deployment |
| FLSM-20 customer sync **Backlog / spec** | FLSM-20 **Post Prod Validation** |
| CRR / transcripts / calendar / shared views thin or missing | Full Zendesk automation umbrella + Tier A pages |
| SellSmart / D2S thin | SellSmart program hub + Digital-to-Store page; REST tool still local WIP |
| SofaScope “live pilot” framing only | Status table refreshed; epic FLSI-2103 still **Testing** |

## Cluster summaries

### ClearView / FLSP-103 (79)

Initiative **In Progress** with four epics: Discovery + Design **Done**; FLSP-159 **Post Prod Validation**; Build **In Progress**. Hosted path delivered AWS hosting, RDS parity/delta sync (full-scale ~2026-06-22), Entra SSO, Approach export (FLSP-508 Done), CI gate.

**Open (sample):** FLSP-390 Backlog (mobile); FLSP-391/403 Testing; bugs FLSP-565/784; hardening FLSP-412/728/783. FLSP-384 is **Done** in live Jira (umbrella keep-open superseded — [[decisions/clearview-flsp384-umbrella.md]]).

| Role | Pages |
|------|-------|
| Initiative | [[initiatives/flsp-103-inventory-lookup.md]] |
| Product hub | [[production-systems/inventory-lookup-clearview.md]] |
| Subsystems | [[production-systems/clearview-aws-hosting.md]] · [[production-systems/clearview-rds-delta-sync.md]] · [[production-systems/approach-reporting.md]] · [[production-systems/pilot-database-migration.md]] |
| Integrations | [[integrations/clearview-entra-sso.md]] · [[integrations/fls-aws-topology.md]] · [[integrations/netsuite-suitetalk-jwt.md]] |
| Techniques | [[techniques/rds-delta-sync-watermarks.md]] · [[techniques/vmpn-serial-snapshot.md]] |
| ADRs | [[decisions/clearview-approach-export-scope.md]] · [[decisions/clearview-location-movement-deferred.md]] · [[decisions/clearview-flsp384-umbrella.md]] · [[decisions/authjs-v5-authorized-callback.md]] |

### Zendesk automation (108)

Nearly closed cluster (≈106/2). Routing (CRR + dedicated agent), shared views, calendar, returns, call transcripts, and NS→ZD customer sync now have wiki homes. Residual: FLSI-2965 Ready for Deployment; OAuth refresh FLSM-24/27 (reporter; Oct 27, 2026).

| Role | Pages |
|------|-------|
| Umbrella | [[initiatives/zendesk-automation-platform.md]] |
| Systems | [[production-systems/crr-round-robin.md]] · [[production-systems/dedicated-agent-assignment.md]] · [[production-systems/zendesk-shared-views.md]] · [[production-systems/zendesk-ticket-calendar.md]] · [[production-systems/zendesk-call-transcripts.md]] · [[production-systems/zendesk-returns-reporting.md]] |
| Integration | [[integrations/netsuite-zendesk-customer-sync.md]] |
| Open | [[open-questions/zendesk-oauth-refresh-2026-10.md]] |

### SellSmart / Copilot / DC Discovery (42)

SellSmart core + analytics Done-ish; FLSM-10 Copilot maintenance **In Progress**; monthly NS→KB refreshes (FLSM-5/25/36) Done; FLSP-85–89 Discovery still open; live NetSuite REST tool remains local WIP.

| Role | Pages |
|------|-------|
| Program | [[initiatives/sellsmart-program.md]] |
| Deep | [[production-systems/sellsmart-copilot.md]] · [[integrations/sellsmart-netsuite-rest-tool.md]] |

### Digital-to-Store / FLSP-247 (6)

Customer-facing Copilot agents (Popdock/SuiteQL). Epic still **Testing**; frontier stories Ready for Deployment vs memory DONE — flagged on the production-system page.

Hub: [[production-systems/digital-to-store-copilot.md]]

### SofaScope (93)

Visual search cluster mostly Done-ish; epic FLSI-2103 **Testing**; tweaks FLSI-2593 **Ready for Deployment**; training video Done; Copilot tool FLSI-3004 **Backlog**. Dense 93-key list lives in cluster-map / assignee catalog — wiki keeps a light related-keys table.

Hub: [[production-systems/sofascope.md]]

## Methodology + interview (Task 8)

| Page | Role |
|------|------|
| [[methodology/neutral-history-framing.md]] | Neutral who-did-what framing |
| [[methodology/verify-against-source-docs.md]] | Verify closeability vs Confluence/SharePoint |
| [[interview-prep/system-design-clearview.md]] | Hosted Next.js + RDS + NetSuite design story |
| [[interview-prep/behavioral-fls-delivery.md]] | Spec-driven Jira, stakeholder loops, prod incidents |

## Tier C catalog (period)

No dedicated wiki pages — rows only.

### ITT / service desk

| Key | Status | Updated | Summary |
|-----|--------|---------|---------|
| [ITT-7512](https://furniturelandsouth.atlassian.net/browse/ITT-7512) | Closed | 2026-05-08 | Ticket #49414 (Jaylon & Cameron) |
| [ITT-8350](https://furniturelandsouth.atlassian.net/browse/ITT-8350) | Closed | 2026-06-17 | Ticket #53222 — Wesley Hall / Peretti |
| [ITT-8351](https://furniturelandsouth.atlassian.net/browse/ITT-8351) | Resolved | 2026-06-11 | Ticket #54468 — Sunset West case |

### Adjacent Zendesk / KB (catalog-only under umbrella)

KB gaps, case-initiator dashboard, Stella bot, messaging triggers — indexed on [[initiatives/zendesk-automation-platform.md]] or SellSmart program; not promoted to Tier A.

## Open threads entering late July 2026

- ClearView Build: FLSP-391/403 Testing; mobile FLSP-390; bugs 565/784; FLSP-384 Done (Jira)
- Zendesk: FLSI-2965 deploy; BusyLight OAuth by **2026-10-27**
- SellSmart: FLSM-10 In Progress; FLSP-85–89 Discovery; REST tool WIP
- D2S: FLSP-247 Testing; frontier Ready for Deployment
- SofaScope: epic Testing; FLSI-2593 Ready for Deployment; FLSI-2599 Familiar Banner Backlog

## Portfolio / interview angles

1. **Hosted enterprise product** — ClearView: Next.js + Entra + ECS + RDS delta sync + role-gated Approach export.
2. **Zendesk automation platform** — CRR, dedicated agent, transcripts, calendar, customer sync as one coherent ops layer.
3. **Spec-driven delivery** — Jira trees + ADRs (FLSP-384 umbrella, Approach scope, Auth.js callback).
4. **Visual search + Copilot** — SofaScope CLIP+FAISS alongside SellSmart / Digital-to-Store agents.

## Hub index (Tasks 1–8)

**Initiatives:** [[initiatives/flsp-103-inventory-lookup.md]] · [[initiatives/zendesk-automation-platform.md]] · [[initiatives/sellsmart-program.md]]

**ClearView:** [[production-systems/inventory-lookup-clearview.md]] · [[production-systems/clearview-aws-hosting.md]] · [[production-systems/clearview-rds-delta-sync.md]] · [[production-systems/approach-reporting.md]] · [[production-systems/pilot-database-migration.md]] · [[integrations/clearview-entra-sso.md]] · [[integrations/fls-aws-topology.md]] · [[integrations/netsuite-suitetalk-jwt.md]] · [[techniques/vmpn-serial-snapshot.md]] · [[techniques/rds-delta-sync-watermarks.md]] · [[decisions/clearview-approach-export-scope.md]] · [[decisions/clearview-location-movement-deferred.md]] · [[decisions/clearview-flsp384-umbrella.md]] · [[decisions/authjs-v5-authorized-callback.md]]

**Zendesk:** [[production-systems/crr-round-robin.md]] · [[production-systems/dedicated-agent-assignment.md]] · [[production-systems/zendesk-call-transcripts.md]] · [[production-systems/zendesk-shared-views.md]] · [[production-systems/zendesk-ticket-calendar.md]] · [[production-systems/zendesk-returns-reporting.md]] · [[integrations/netsuite-zendesk-customer-sync.md]] · [[open-questions/zendesk-oauth-refresh-2026-10.md]]

**SellSmart / D2S / SofaScope:** [[initiatives/sellsmart-program.md]] · [[production-systems/sellsmart-copilot.md]] · [[integrations/sellsmart-netsuite-rest-tool.md]] · [[production-systems/digital-to-store-copilot.md]] · [[production-systems/sofascope.md]]

**Methodology / interview:** [[methodology/neutral-history-framing.md]] · [[methodology/verify-against-source-docs.md]] · [[interview-prep/system-design-clearview.md]] · [[interview-prep/behavioral-fls-delivery.md]]

## Sources

- `raw/fls-work/jira/2026-07-21/AUDIT_REPORT.md`
- `raw/fls-work/jira/2026-07-21/cluster-map.md`
- `raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md`
- Task 1–8 wiki hubs (2026-07-21 catch-up)
