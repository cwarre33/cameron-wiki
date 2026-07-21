---
title: SellSmart Copilot Studio Tools
type: production-system
status: active
visibility: fls-internal
sources:
  - repo:SellSmartTools
  - bitbucket:sellsmart-tools
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - raw/fls-work/jira/2026-07-21/cluster-map.md
  - raw/fls-work/sellsmart/2026-07-21/MEMORY.md
related:
  - "[[initiatives/sellsmart-program.md]]"
  - "[[integrations/sellsmart-netsuite-rest-tool.md]]"
  - "[[production-systems/digital-to-store-copilot.md]]"
  - "[[production-systems/sofascope.md]]"
created: 2026-05-20
updated: 2026-07-21
confidence: high
tags: [sellsmart, copilot-studio, netsuite, dataverse, fls, production]
---

# SellSmart Copilot Studio Tools

Tooling for the **SellSmart** Microsoft Copilot Studio bot at FLS — syncing NetSuite product data into the knowledge base, diagnosing conversations, generating improvement suggestions, and (WIP) live NetSuite REST queries.

**Repo:** `CleanDevEnvironment/SellSmartTools/` (Bitbucket: `furniturelandsouth/sellsmart-tools`)

**Program hub:** [[initiatives/sellsmart-program.md]]

**Status refresh (2026-07-21):** Core epic [FLSI-2333](https://furniturelandsouth.atlassian.net/browse/FLSI-2333) **Done**; Analytics epic [FLSI-2869](https://furniturelandsouth.atlassian.net/browse/FLSI-2869) **Done**; maintenance epic [FLSM-10](https://furniturelandsouth.atlassian.net/browse/FLSM-10) **In Progress** with monthly refreshes FLSM-5/25/36 **Done**. DC Furniture Discovery FLSP-85–89 still open under FLSP-84.

Customer-facing Copilot (different product): [[production-systems/digital-to-store-copilot.md]].

## Package architecture

| Package | Purpose | Data flow |
|---------|---------|-----------|
| **sellsmart-datasync** | SuiteQL/ODBC extract → CSV → Dataverse knowledge base upload | NetSuite → Copilot KB (batch) |
| **sellsmart-diagnostics** | Transcript analysis + live M365 Copilot Chat API queries | Copilot → analytics JSON |
| **sellsmart-improvements** | Topic YAML + diagnostics → LLM improvement suggestions | Analytics → actionable YAML |
| **sellsmart-netsuite-rest-tool** | OpenAPI 3 REST tool for live SuiteQL/inventory | NetSuite → Copilot (real-time) |

## Datasync pattern

- Extracts via NetSuite ODBC (`NSODBC_NETSUITE2_DSN`) or SuiteQL scripts
- Uploads to Copilot knowledge base via Power Platform CLI (`pac`)
- **Safe replace:** new files uploaded first; old versions deleted only after replacement confirmed
- Joins product hierarchy: `CUSTOMLIST_PRODUCT_CLASSES`, `CUSTOMRECORD_PRODUCT_CATEGORY_TIER2`, vendor web name records
- **Ops cadence:** monthly KB sync / NetSuite data refresh stories under FLSM-10 (FLSM-5, FLSM-25, FLSM-36 — all Done through July 2026)

## Diagnostics + improvements loop

1. **Diagnostics** produces session analytics: resolution/escalation/abandon rates per topic
2. **Improvements** consumes topic YAML + analytics, generates LLM-assisted fixes
3. Parser tests + apply script for topic YAML updates (FLSI-2869 Analytics epic **Done**; FLSI-2887–2889 Deployed/Done)

## LLM providers (improvements)

Configurable: NVIDIA NIM, OpenAI, or Azure OpenAI via root `.env`.

## Live REST tool (still WIP)

- Package **`sellsmart-netsuite-rest-tool/`** — OpenAPI spec + Copilot setup docs (local WIP as of May 2026 work-log; not contradicted by July Jira freeze)
- Complements static CSV KB with live SuiteQL / inventory for Design Consultants
- See [[integrations/sellsmart-netsuite-rest-tool.md]]

## Interview angles

- **Hybrid RAG architecture:** Static CSV knowledge base for bulk catalog + REST tool for live inventory (when deployed)
- **Safe KB updates:** Upload-then-delete pattern prevents Copilot knowledge gaps during sync
- **Closed-loop improvement:** Diagnostics → LLM suggestions → YAML apply pipeline
- **Program vs product:** FLSI-2333 Done while FLSM-10 stays open for monthly ops + FLSP-85–89 discovery
