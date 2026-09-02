---
title: Decision — Shop Request Duplicate Guard
type: decision
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-09-02/flsp-856-epic-tree.md
  - raw/fls-work/jira/2026-09-02/flsp-856-story-descriptions.md
  - raw/fls-work/git/2026-09-02/inventory-lookup/adr-signals.json
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp1162_shop_create_barcode_check.md
related:
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
  - "[[decisions/clearview-shop-live-netsuite-read.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [decision, clearview, shop, duplicate-prevention]
---

# Decision — Shop Request Duplicate Guard

**Context:** Creating Shop Requests from ClearView (and eventually from status/location triggers) must not open a second active request for the same barcode.

**Decision:** Before create, check for an **open** Shop Request on that barcode. If one exists, block create and link the user to the existing request.

Also validate the barcode exists in inventory before create (separate create-form guard).

**Status:** Done in app; same rule is acceptance criteria for the NetSuite create/close automation still In Progress.

**Consequences:** Operators always land on the live request instead of forking history. Closed requests do not block a new open cycle.
