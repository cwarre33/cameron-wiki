---
title: Zendesk Automation Platform
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/cluster-map.md
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/zendesk-tools/2026-07-21-memory.md
  - raw/fls-work/transcripts/2026-07-21-memory.md
related:
  - "[[production-systems/crr-round-robin.md]]"
  - "[[production-systems/dedicated-agent-assignment.md]]"
  - "[[production-systems/zendesk-call-transcripts.md]]"
  - "[[production-systems/zendesk-shared-views.md]]"
  - "[[production-systems/zendesk-ticket-calendar.md]]"
  - "[[production-systems/zendesk-returns-reporting.md]]"
  - "[[integrations/netsuite-zendesk-customer-sync.md]]"
  - "[[open-questions/zendesk-oauth-refresh-2026-10.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [initiative, jira-index, zendesk]
---

# Zendesk Automation Platform

Umbrella index for Cameron's Zendesk automation cluster at Furnitureland South — routing (CRR / dedicated agent), agent-status jobs, shared views, call transcripts, calendar app, returns reporting, and NetSuite↔Zendesk customer sync.

**Jira footprint (2026-07-21 cluster map):** **108** assignee issues (30 stories+/non-subtasks, 78 sub-tasks). Done-ish / open-ish ≈ **106 / 2**.

**Repo root:** `CleanDevEnvironment/Zendesk/ZendeskTools/` (DedicatedAgentAssignment, ZendeskSharedViews, ZendeskTicketCalendar, ZendeskCallAutoTranscript, ZendeskWaitTimeServer, …).

This page is Tier B navigation. Deep synthesis lives on the linked production-system / integration pages.

## Systems map

| System | Wiki page | Primary keys | Status (live/catalog 2026-07-21) |
|--------|-----------|--------------|----------------------------------|
| CRR / CCS–VCS round robin | [[production-systems/crr-round-robin.md]] | FLSI-2066, FLSI-3032, FLSM-33 | Done (post-launch FLSI-2965 still open) |
| Dedicated agent assignment | [[production-systems/dedicated-agent-assignment.md]] | FLSP-163, FLSP-162, FLSI-2965 | FLSP-163 **Done**; FLSI-2965 Ready for Deployment |
| Shared views cleanup | [[production-systems/zendesk-shared-views.md]] | FLSI-2968 | Done |
| Call transcripts | [[production-systems/zendesk-call-transcripts.md]] | FLSI-2761–2765, FLSI-2973/2990–2994 | Done (durable pipeline; thin early Jira) |
| Due Dates Calendar App | [[production-systems/zendesk-ticket-calendar.md]] | FLSP-68, FLSI-2881 | Done |
| Returns reporting (D2K + Choros) | [[production-systems/zendesk-returns-reporting.md]] | FLSP-102 / 132 / 133 | Done |
| NS → Zendesk customer sync | [[integrations/netsuite-zendesk-customer-sync.md]] | FLSM-20 | **Post Prod Validation** |

## Stories+ key index (compact)

Cluster-map stories+/non-subtasks only — not the 78 sub-tasks. Statuses from assignee catalog (refreshed via live Jira where noted).

### Routing & CRR

| Key | Summary | Status |
|-----|---------|--------|
| [FLSI-2066](https://furniturelandsouth.atlassian.net/browse/FLSI-2066) | Round Robin CCS Dedicated agent | **Done** (live) |
| [FLSI-3032](https://furniturelandsouth.atlassian.net/browse/FLSI-3032) | Custom Round Robin R&D | Done |
| [FLSI-2965](https://furniturelandsouth.atlassian.net/browse/FLSI-2965) | Round Robin CCS Dedicated agent [POST LAUNCH] | **Ready for Deployment** (live) |
| [FLSM-33](https://furniturelandsouth.atlassian.net/browse/FLSM-33) | Vendor RR tickets count toward daily cap | Done |
| [FLSP-160](https://furniturelandsouth.atlassian.net/browse/FLSP-160) | Scope Out Weimer's Request (epic) | Done |
| [FLSP-162](https://furniturelandsouth.atlassian.net/browse/FLSP-162) | Create Dedicated Agent Organization Field | Done |
| [FLSP-163](https://furniturelandsouth.atlassian.net/browse/FLSP-163) | Org dedicated-agent logic in CRR | **Done** (live) — ⚠️ wiki previously said Testing |
| [FLSP-138](https://furniturelandsouth.atlassian.net/browse/FLSP-138) | Fix Set Agents Online.bat retry logic | Done |
| [FLSP-81](https://furniturelandsouth.atlassian.net/browse/FLSP-81) | Set all agents ticket access to All Tickets | Done |

### Views, calendar, returns, sync

| Key | Summary | Status |
|-----|---------|--------|
| [FLSI-2968](https://furniturelandsouth.atlassian.net/browse/FLSI-2968) | Zendesk Views Clean-Up | **Done** (live) |
| [FLSP-68](https://furniturelandsouth.atlassian.net/browse/FLSP-68) | Due Dates Calendar App (epic) | **Done** (live) |
| [FLSI-2881](https://furniturelandsouth.atlassian.net/browse/FLSI-2881) | Create App for Testing (calendar) | Done |
| [FLSP-102](https://furniturelandsouth.atlassian.net/browse/FLSP-102) | Zendesk Returns Reporting (epic) | Done |
| [FLSP-132](https://furniturelandsouth.atlassian.net/browse/FLSP-132) / [FLSP-133](https://furniturelandsouth.atlassian.net/browse/FLSP-133) | Choros / Francisco D2K | Done |
| [FLSM-20](https://furniturelandsouth.atlassian.net/browse/FLSM-20) | Replace SmartConnect Customer Sync | **Post Prod Validation** (live) |

### Transcripts / AWS follow-ons (also in Zendesk cluster)

| Key | Summary | Status |
|-----|---------|--------|
| [FLSI-2761](https://furniturelandsouth.atlassian.net/browse/FLSI-2761) / [FLSI-2762](https://furniturelandsouth.atlassian.net/browse/FLSI-2762) | Local Whisper backfill + model eval | Done |
| [FLSI-2763](https://furniturelandsouth.atlassian.net/browse/FLSI-2763)–[FLSI-2765](https://furniturelandsouth.atlassian.net/browse/FLSI-2765) | AWS architecture / PoC / cost review | Done |
| [FLSI-2973](https://furniturelandsouth.atlassian.net/browse/FLSI-2973), [FLSI-2990](https://furniturelandsouth.atlassian.net/browse/FLSI-2990)–[FLSI-2994](https://furniturelandsouth.atlassian.net/browse/FLSI-2994) | Task Server job, test, docs, upload check | Done |

### Adjacent Zendesk work (same cluster, lighter wiki depth)

| Key | Summary | Status |
|-----|---------|--------|
| [FLSI-1842](https://furniturelandsouth.atlassian.net/browse/FLSI-1842) | Agent-focused procedures / AI-ready articles | Deployed to Prod |
| [FLSI-1979](https://furniturelandsouth.atlassian.net/browse/FLSI-1979) / [FLSI-1980](https://furniturelandsouth.atlassian.net/browse/FLSI-1980) | Response accuracy / flow enhancements | Done |
| [FLSI-2039](https://furniturelandsouth.atlassian.net/browse/FLSI-2039) | Messaging triggers/goals | Abandoned |
| [FLSI-2670](https://furniturelandsouth.atlassian.net/browse/FLSI-2670) | KB gaps | Done |
| [FLSI-2672](https://furniturelandsouth.atlassian.net/browse/FLSI-2672) | Case initiator Dashboard | Done |

## Open residual

- **FLSI-2965** (and child FLSI-3011 Tag Inactive Employees) — still **Ready for Deployment** as of live check 2026-07-21.
- **FLSM-24 / FLSM-27** — Zendesk OAuth refresh for custom apps (**BusyLight**); hard deadline **Oct 27, 2026**. Reporter work; assignee John. See [[open-questions/zendesk-oauth-refresh-2026-10.md]].
- Cluster map open-ish count ≈ 2; treat catalog + live Jira as source of truth for any new reopenings.

## Contradiction log

- **FLSP-163:** May-2026 wiki said **Testing**; Jira (catalog + live 2026-07-21) is **Done**. Corrected on [[production-systems/dedicated-agent-assignment.md]].
- **FLSM-20:** May-2026 wiki said **Backlog / planned**; live Jira is **Post Prod Validation**. Corrected on [[integrations/netsuite-zendesk-customer-sync.md]].
