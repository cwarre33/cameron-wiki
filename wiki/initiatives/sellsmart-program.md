---
title: SellSmart Program
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
  - raw/fls-work/jira/2026-07-21/AUDIT_REPORT.md
  - raw/fls-work/sellsmart/2026-07-21/MEMORY.md
  - wiki/production-systems/sellsmart-copilot.md
  - wiki/integrations/sellsmart-netsuite-rest-tool.md
related:
  - "[[production-systems/sellsmart-copilot.md]]"
  - "[[integrations/sellsmart-netsuite-rest-tool.md]]"
  - "[[production-systems/digital-to-store-copilot.md]]"
  - "[[integrations/netsuite-suitetalk-jwt.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [initiative, jira-index, sellsmart, copilot-studio, furnitureland-south]
---

# SellSmart Program

Tier B navigation hub for Cameron's **SellSmart / Copilot / DC Furniture Discovery** cluster at Furnitureland South — Design Consultant Copilot tooling, analytics loop, monthly NetSuite KB refreshes, and the next-wave furniture discovery stories.

**Jira footprint (2026-07-21 cluster map):** **42** assignee issues (20 stories+/non-subtasks, 22 sub-tasks). Done-ish / open-ish ≈ **33 / 9**.

**Deep pages:** [[production-systems/sellsmart-copilot.md]] (packages + ops) · [[integrations/sellsmart-netsuite-rest-tool.md]] (live SuiteQL OpenAPI WIP).

**Adjacent (customer Copilot, not DC SellSmart):** [[production-systems/digital-to-store-copilot.md]] (FLSP-247).

## Systems map

| Workstream | Wiki / notes | Primary keys | Status (live/catalog 2026-07-21) |
|------------|--------------|--------------|----------------------------------|
| SellSmart core epic | [[production-systems/sellsmart-copilot.md]] | FLSI-2333 | **Done** |
| DC requests / topics | sellsmart-copilot topics | FLSI-2468 (+ sub-tasks) | **Done** (most Deployed; FLSI-2865 Backlog) |
| Synchronous vendor data | sellsmart-copilot | FLSI-2760 | **Done** |
| SellSmart Analytics | sellsmart-copilot diagnostics/improvements | FLSI-2869, FLSI-2887–2889 | **Done** |
| Copilot maintenance epic | monthly refreshes below | FLSM-10 | **In Progress** |
| Monthly NS → KB sync | datasync ops | FLSM-5, FLSM-25, FLSM-36 | **Done** (May/June/July cycles) |
| DC Furniture Discovery | next capability under FLSP-84 | FLSP-85–89 | Open (Backlog / In Progress) |
| Live NetSuite REST tool | [[integrations/sellsmart-netsuite-rest-tool.md]] | (repo WIP; not a Jira epic in this cluster) | Local WIP (May 2026) |
| SofaScope Copilot tool | SofaScope backlog (Task 6) | FLSI-3004 | **Backlog** — catalog only here |

## Epic / story index (stories+)

### Core SellSmart (FLSI)

| Key | Summary | Status |
|-----|---------|--------|
| [FLSI-2333](https://furniturelandsouth.atlassian.net/browse/FLSI-2333) | SellSmart (epic) | **Done** (live) |
| [FLSI-2468](https://furniturelandsouth.atlassian.net/browse/FLSI-2468) | DC's Requests | Done |
| [FLSI-2726](https://furniturelandsouth.atlassian.net/browse/FLSI-2726) | Refresh Netsuite Data | Done |
| [FLSI-2760](https://furniturelandsouth.atlassian.net/browse/FLSI-2760) | Implement Synchronous Vendor Data | Done |
| [FLSI-2869](https://furniturelandsouth.atlassian.net/browse/FLSI-2869) | SellSmart Analytics (epic) | **Done** (live) |
| [FLSI-2887](https://furniturelandsouth.atlassian.net/browse/FLSI-2887) | Plug & Play Testing of New Topic YAMLs | Done |
| [FLSI-2888](https://furniturelandsouth.atlassian.net/browse/FLSI-2888) | Define deployment pipeline for improved topics | Done |
| [FLSI-2889](https://furniturelandsouth.atlassian.net/browse/FLSI-2889) | Extend analytics for topic funnel metrics | Done |

### Copilot maintenance + monthly refreshes (FLSM)

| Key | Summary | Status |
|-----|---------|--------|
| [FLSM-10](https://furniturelandsouth.atlassian.net/browse/FLSM-10) | Copilot (epic) | **In Progress** (live) |
| [FLSM-5](https://furniturelandsouth.atlassian.net/browse/FLSM-5) | SellSmart Knowledge Base Monthly Sync | **Done** |
| [FLSM-25](https://furniturelandsouth.atlassian.net/browse/FLSM-25) | June SellSmart NetSuite Data Refresh | **Done** |
| [FLSM-36](https://furniturelandsouth.atlassian.net/browse/FLSM-36) | July SellSmart NetSuite Data Refresh | **Done** |

FLSM-10 stays open as the maintenance umbrella while monthly refresh stories close.

### DC Furniture Discovery (FLSP-84 children)

| Key | Summary | Status |
|-----|---------|--------|
| [FLSP-85](https://furniturelandsouth.atlassian.net/browse/FLSP-85) | Define DC Furniture Discovery Use Cases | **Backlog** |
| [FLSP-86](https://furniturelandsouth.atlassian.net/browse/FLSP-86) | Define Data Sources for Furniture Guidance | **In Progress** |
| [FLSP-87](https://furniturelandsouth.atlassian.net/browse/FLSP-87) | Design SellSmart Copilot Guidance Behavior | **In Progress** |
| [FLSP-88](https://furniturelandsouth.atlassian.net/browse/FLSP-88) | Implement Initial Furniture Discovery Capability | **In Progress** |
| [FLSP-89](https://furniturelandsouth.atlassian.net/browse/FLSP-89) | Validate with DC Feedback | **In Progress** |

Parent epic/story **FLSP-84** is outside Cameron's assignee catalog for this freeze — linked only as parent of FLSP-85–89.

### Cluster-adjacent (light)

| Key | Summary | Status | Note |
|-----|---------|--------|------|
| [FLSI-2623](https://furniturelandsouth.atlassian.net/browse/FLSI-2623) | Stella Bot on front page during Off Hours | Deployed to Prod | Clustered under SellSmart; no dedicated wiki page |
| [FLSI-2755](https://furniturelandsouth.atlassian.net/browse/FLSI-2755) | Zendesk Copilot App | Ready for Deployment | Catalog only |
| [FLSI-3004](https://furniturelandsouth.atlassian.net/browse/FLSI-3004) | SofaScope Copilot Tool | Backlog | Belongs with SofaScope (Task 6) |

## Open residual

- **FLSM-10** — Copilot maintenance epic still **In Progress** despite closed monthly refresh stories.
- **FLSP-85–89** — DC Furniture Discovery still open (one Backlog, four In Progress).
- **FLSI-2865** — "Reinforce Trust and Transparency Principles" still **Backlog** under FLSI-2468.
- **sellsmart-netsuite-rest-tool** — still local WIP per May wiki / work-log; not contradicted by this Jira freeze.

## Contradiction log

- None vs prior wiki pages. May-2026 [[production-systems/sellsmart-copilot.md]] framed REST tool as uncommitted WIP — still accurate.
- Digital-to-Store frontier memory saying FLSP-248/249/251 "DONE" vs Jira **Ready for Deployment** is documented on [[production-systems/digital-to-store-copilot.md]], not a SellSmart conflict.
