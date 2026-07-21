---
title: NetSuite SuiteTalk JWT (ClearView Pattern)
type: integration
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_netsuite_auth.md
  - raw/fls-work/clearview-memory/2026-07-21/project_inventory_lookup.md
  - raw/fls-work/clearview-memory/2026-07-21/project_delta_sync_build.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[integrations/sellsmart-netsuite-rest-tool.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [netsuite, suitetalk, suiteql, jwt, oauth, ps256, clearview, furnitureland-south]
---

# NetSuite SuiteTalk JWT (ClearView Pattern)

ClearView talks to NetSuite via **SuiteTalk REST + SuiteQL** authenticated with **OAuth 2.0 JWT (PS256)** — not ODBC — so the same client runs in local Node, containers, and CI-shaped environments without native DSN drivers.

**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]

## Why JWT SuiteTalk (not ODBC)

| Concern | SuiteTalk JWT | ODBC (sibling pattern) |
|---------|---------------|------------------------|
| Runtime | Pure Node (`jsrsasign` JWT) | Local driver + DSN |
| Deploy | Works in ECS/Fargate | Friction in containers |
| Used by | ClearView live queries + delta lanes | ItemInventoryStory / **ja-utility-shed**-style extracts |

ClearView intentionally does **not** copy ODBC patterns from ja-utility-shed for primary data access. Optional SuiteAnalytics ODBC remains a **fallback** for support-case notes when the JWT role cannot see required fields — not the default path.

## Auth flow

1. Build JWT signed **PS256** (certificate private key + certificate id + consumer key / account)
2. Exchange at SuiteTalk token endpoint → bearer token
3. Cache token in-memory until expiry
4. `POST /services/rest/query/v1/suiteql` via `querySuiteQL(sql, limit)` in `lib/netsuite.ts`
5. Strip `links` metadata keys from row results

Env surface (high level): account id, production/sandbox flags, consumer key, certificate id, private key.

## Where it shows up in ClearView

- Live barcode/timeline SuiteQL when configured
- All multi-lane delta sync discover/extract paths ([[production-systems/clearview-rds-delta-sync.md]]) — cloud-agnostic SuiteQL, no ODBC dependency for sync packaging
- SellSmart Copilot REST tool shares the same tenant/SuiteQL idea but is a separate OpenAPI surface — [[integrations/sellsmart-netsuite-rest-tool.md]]

## Gotchas

- SuiteQL REST **offset cap ~999,000** — use keyset/seek pagination for full-history extracts
- Never filter `lastmodifieddate >= SYSDATE - n` — account vs server TZ skew; derive watermarks from `MAX(lastmodifieddate)`
- Some note columns (`notedate` / `lastmodifieddate`) are **not exposed** on the FLS role → notes lane uses id watermark

## Status

Stable production pattern for ClearView. Prefer this when adding new NetSuite queries to Inventory-Lookup.
