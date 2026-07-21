---
title: Zendesk Returns Reporting (D2K + Choros)
type: production-system
status: active
visibility: fls-internal
sources: [jira:FLSP-102, jira:FLSP-133, jira:FLSP-132]
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
  - "[[production-systems/dedicated-agent-assignment.md]]"
  - "[[integrations/netsuite-zendesk-customer-sync.md]]"
created: 2026-05-20
updated: 2026-07-21
confidence: high
tags: [zendesk, netsuite, reporting, d2k, choros, returns, fls]
---

# Zendesk Returns Reporting (D2K + Choros)

Epic delivering standardized returns/concessions reporting by joining Zendesk CI tickets with NetSuite financial data.

**Jira:** [FLSP-102 Zendesk Returns Reporting](https://furniturelandsouth.atlassian.net/browse/FLSP-102) (Epic, **Done**)

## Child deliverables

| Ticket | Report | Status |
|--------|--------|--------|
| [FLSP-133](https://furniturelandsouth.atlassian.net/browse/FLSP-133) | Francisco D2K Report | Done |
| [FLSP-132](https://furniturelandsouth.atlassian.net/browse/FLSP-132) | Choros Report | Done |

---

## Francisco D2K Report (FLSP-133)

**Objective:** Measure **Discount to Keep (D2K)** per CI agent over a rolling window (e.g., 30 days).

**D2K definition:** Money returned to customer relative to original Sales Order — customer concessions as % and $ of original sale.

**Data strategy:**
- **NetSuite = source of truth** for dollar amounts (credit memos with D2K item, tied to Sales Order)
- Do **not** rely on Zendesk custom fields for dollar amounts
- Scope Zendesk tickets: CI group, relevant tags, case linkage
- Join Zendesk ↔ NetSuite via Sales Order number (+ optional NetSuite case number on ticket)

**Output:**
- Ticket-level dataset (Zendesk + NetSuite attributes)
- Agent-level aggregates: avg D2K %, blended %, total D2K dollars

---

## Choros Report (FLSP-132)

**Objective:** Rebuild legacy damaged/returned inventory SQL as NetSuite SuiteQL with **1:1 column + row parity** against legacy `Query.csv`.

**Implementation:** `javascript/app/netsuite/legacy-damage-return-compare.js`
- Pulls NetSuite via REST SuiteQL in **50-barcode chunks** (timeout avoidance)
- Normalizes output, compares vs legacy CSV with overlap stats + diffs

**Data strategy (split queries):**
1. Dates/customer
2. Item/vendor/cost/tag/process (`inventorynumber` / `item` / `vendor`)
3. Location + reasons — latest `RtnAuth` via `transaction`/`transactionline` + backfill from `customrecord_fls_return_inv(_hdr)`

**Parity achieved:**
- **Barcode parity: 651/652** (only legacy outlier: `4600000000001`)
- `field_parity` summary quantifies column-level mismatches with samples

**Remaining gaps:**
- Location/tag/process/problem/description (often missing on txn-derived rows)
- `customer_id` semantics: legacy `CUST#` vs NetSuite internal ID
- **Next:** Daily email pipeline to Choros with Zendesk ticket alignment

**Local folder:** `CleanDevEnvironment/ChorosReport/` (minimal — settings only; implementation in NetSuite JS repo)

---

## Interview angles

- **Source-of-truth discipline:** Financial amounts from NetSuite, Zendesk for workflow/ticket context only
- **Legacy migration parity:** Quantified field-by-field diff (`field_parity`) before cutting over reports
- **Chunked SuiteQL:** 50-barcode batches to stay within REST timeout limits
