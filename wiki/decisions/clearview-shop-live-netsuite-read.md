---
title: Decision — Shop Requests Read Live from NetSuite (Not RDS)
type: decision
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp942_shop_request_record.md
  - raw/fls-work/inventory-lookup-docs/2026-09-02/specs/2026-08-06-flsp-942-shop-request-record-design.md
  - raw/fls-work/jira/2026-09-02/flsp-856-story-descriptions.md
related:
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[production-systems/clearview-rds-delta-sync.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [decision, clearview, shop, netsuite, rds, architecture]
---

# Decision — Shop Requests Read Live from NetSuite (Not RDS)

**Context:** Inventory browse/detail/orders use the Postgres RDS read plane (~15 min delta lag). Shop/RMF is an **operational queue** — status, notes, and ownership change during a shift. A 15-minute lag is unacceptable for shop-floor work.

**Decision:**

1. **ClearView reads Shop Requests live from NetSuite** (SuiteQL/REST) — no Shop read lane, no RDS table for the queue.
2. **NetSuite `customrecordfls_shop_request` is system of record** (underscore-less script id locked at SB1 creation — not editable after save).
3. Until Blue Yonder / WMS auto-creates records, a **transitional WRITE sync** (iSeries PIE → NetSuite) runs as its own scheduled task, decoupled from `sync-all-delta.ts`.
4. Closed-ticket comment history (~1.99M logical comments) routes to **NSAW**, not bulk NetSuite notes; open-queue comments stay on the live record. On-demand historical load from ClearView — [[production-systems/clearview-shop-rmf-requests.md]].

**Status:** Shipped and live-verified (staging + prod). BY/WMS create/close automation still In Progress.

**Consequences:** Shop APIs depend on NetSuite availability/concurrency (AbortController + retry patterns matter). Do not "fix" Shop freshness by adding an RDS lane without revisiting the ops SLA. Transitional sync retires when BY/WMS owns create.
