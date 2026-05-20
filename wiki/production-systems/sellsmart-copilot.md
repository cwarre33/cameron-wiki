---
title: SellSmart Copilot Studio Tools
type: production-system
status: active
visibility: fls-internal
sources: [repo:SellSmartTools, bitbucket:sellsmart-tools]
related: [[integrations/sellsmart-netsuite-rest-tool.md]], [[production-systems/sofascope.md]]
created: 2026-05-20
updated: 2026-05-20
confidence: high
tags: [sellsmart, copilot-studio, netsuite, dataverse, fls, production]
---

# SellSmart Copilot Studio Tools

Tooling for the **SellSmart** Microsoft Copilot Studio bot at FLS — syncing NetSuite product data into the knowledge base, diagnosing conversations, generating improvement suggestions, and (WIP) live NetSuite REST queries.

**Repo:** `CleanDevEnvironment/SellSmartTools/` (Bitbucket: `furniturelandsouth/sellsmart-tools`)

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

## Diagnostics + improvements loop

1. **Diagnostics** produces session analytics: resolution/escalation/abandon rates per topic
2. **Improvements** consumes topic YAML + analytics, generates LLM-assisted fixes
3. Parser tests + apply script for topic YAML updates (FLSI-2869 refactor, Feb 2026)

## LLM providers (improvements)

Configurable: NVIDIA NIM, OpenAI, or Azure OpenAI via root `.env`.

## May 2026 WIP

- New **`sellsmart-netsuite-rest-tool/`** package (uncommitted) — OpenAPI spec + Copilot setup docs
- `sellsmart-datasync/scripts/update-copilot-knowledge-sources.js` modified
- Root README updated with REST tool package row

See [[integrations/sellsmart-netsuite-rest-tool.md]] for live API tool details.

## Interview angles

- **Hybrid RAG architecture:** Static CSV knowledge base for bulk catalog + REST tool for live inventory (when deployed)
- **Safe KB updates:** Upload-then-delete pattern prevents Copilot knowledge gaps during sync
- **Closed-loop improvement:** Diagnostics → LLM suggestions → YAML apply pipeline
