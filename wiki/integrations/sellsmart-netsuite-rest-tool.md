---
title: SellSmart NetSuite REST Tool (Copilot Studio)
type: integration
status: active
visibility: fls-internal
sources: [repo:SellSmartTools/sellsmart-netsuite-rest-tool]
related: [[production-systems/sellsmart-copilot.md]], [[production-systems/inventory-lookup-clearview.md]]
created: 2026-05-20
updated: 2026-05-20
confidence: high
tags: [sellsmart, copilot-studio, netsuite, openapi, suiteql, rest, live-inventory]
---

# SellSmart NetSuite REST Tool (Copilot Studio)

OpenAPI 3 specification enabling the SellSmart Copilot agent to query **live NetSuite data** — complementing the static CSV knowledge base from datasync.

**Repo:** `SellSmartTools/sellsmart-netsuite-rest-tool/`

**Status:** Local WIP (uncommitted, May 2026)

## Three REST operations

| Operation ID | NetSuite endpoint | Purpose |
|--------------|-------------------|---------|
| `getProductContextView` | `POST /query/v1/suiteql` | Joined item view: class, category, vendor, attributes |
| `getFieldOptions` | `GET /record/v1/customlist/{listId}` | Valid values for custom list fields |
| `getInventoryTiers` | `GET .../inventoryItem/{id}/inventoryDetail` | Per-location availability vs backorder |

## Design Consultant disclaimers (built into spec)

- Stock is **as of last API read** — state clearly to customers
- Document gaps from DATA_AUDIT (floor samples, lag, excluded locations)
- Do not imply 100% accuracy when audit identifies blind spots

## Pre-deployment checklist

1. Complete **DATA_AUDIT.md** — field internal IDs, hierarchy, inventory lag, documented gaps
2. Validate OpenAPI: `npx @apidevtools/swagger-cli validate openapi/sellsmart-netsuite-copilot.yaml`
3. Prototype OAuth in **PROTOTYPE_REST.md** (curl/Postman)
4. Upload spec to Copilot Studio REST API tool (max 5 MB)
5. Configure OAuth 2.0 Bearer token (NetSuite JWT client credentials)
6. Run DC acceptance scenarios from **COPILOT_STUDIO_SETUP.md**

## DATA_AUDIT focus areas

- Product class (`class` → `CUSTOMLIST_PRODUCT_CLASSES`)
- Category tier 2 (`custitem_product_category_tier2`)
- Vendor web name (`custitem_vendor_web_name`)
- Style/material fields — **TBD**, must confirm via Show Internal IDs
- Inventory lag measurement (API vs UI comparison)
- Showroom floor sample detection gap

## Fallback: BFF pattern

If Copilot Studio cannot perform NetSuite JWT client-credentials flow, deploy a backend-for-frontend holding secrets and exposing the same three operation IDs unchanged.

## Relationship to Inventory Lookup

Both projects use SuiteQL against the same NetSuite tenant. Inventory Lookup is stakeholder-facing barcode intelligence; this tool is Copilot-facing product/inventory queries for Design Consultants.

## Interview angles

- **Static vs live data split:** CSV KB for breadth, REST for freshness-critical inventory
- **OpenAPI as contract:** Copilot Studio consumes spec directly — audit-first field discovery
- **Operational honesty:** Explicit disclaimers in API description reduce hallucinated certainty
