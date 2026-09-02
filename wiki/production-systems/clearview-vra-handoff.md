---
title: ClearView VRA Handoff
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-09-02/flsp-856-story-descriptions.md
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp782_vra_handoff.md
  - raw/fls-work/inventory-lookup-docs/2026-09-02/
  - raw/fls-work/git/2026-09-02/inventory-lookup/adr-signals.json
  - repo:NetSuite/Inventory-Lookup
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[work-log/2026-08-09-clearview-shop-rmf-sprint.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [clearview, vra, netsuite, suitelet, furnitureland-south]
---

# ClearView VRA Handoff

**Create Vendor Return** from ClearView item detail → NetSuite VRA Suitelet. Lives under the Development epic (adjacent to PIE & Shop), but is part of the ClearView ops story.

**Status:** Post Prod Validation (as of 2026-09-02)

## Problem

Original handoff passed the source PO's NetSuite internal id. That **broke** for barcodes whose Item Receipt path goes Return Authorization → Sales Order with **no PO** in history.

## What shipped

1. **Availability gate** — action greyed with reason for `on_order` / `not_available`; enabled for `available` / `reserved`; hidden when no barcode.
2. **Barcode-based Suitelet intake** (2026-08-27) — URL keyed by scriptid/deployid + `barcode=` (not numeric script ids + `po=`). Unblocks RA/SO-no-PO cases entirely.
3. ClearView builds the URL from the serial's barcode; Easy Tags–style gate on barcode presence.

## False-start lesson (worth remembering)

A verbal claim that NetSuite "already supports barcode intake" was not the same as a shipped contract. Suitelet `on_request` source looked unchanged because the real change lived in a **compiled React File Cabinet bundle**. Live URL tests + reading the right artifact beat re-reading the wrong source.

## Still open

- Suitelet base URL still points at **SB1** until the script promotes — flip to production account host when ready.
- Dead PO-linkage pipeline left in place on purpose (RBAC + SQL join + verify scripts); cleanup is a separate ask.

## Scope note

Orders-page VRA action: **not** required unless further notice (stakeholder steer).

## Interview angle

Contract verification across NetSuite File Cabinet artifacts; designing handoff URLs that don't assume a PO exists on every serial history.
