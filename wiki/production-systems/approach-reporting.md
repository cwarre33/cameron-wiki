---
title: Approach Reporting (ClearView Export)
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp508_approach_reporting.md
  - raw/fls-work/clearview-memory/2026-07-21/reference_approach_report_docs.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [clearview, approach, export, csv, xlsx, rbac, flsp-508, furnitureland-south]
---

# Approach Reporting (ClearView Export)

ClearView's successor to FLS's legacy **Approach** inventory-reporting tool: filtered CSV/XLSX export from `/items` with role-gated pricing columns.

**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]  
**Jira:** [FLSP-508](https://furniturelandsouth.atlassian.net/browse/FLSP-508) **Done** (2026-07-21, PR #58)

## Purpose

Preserve Approach's core job — broad/partial-info investigation → flexible column export — without rebuilding every legacy pivot/PDF template. Discovery origin: FLSP-137 / FLSP-109 legacy analysis.

## What shipped

| Capability | Notes |
|------------|-------|
| CSV + Excel | Flat serial export + **grouped-by-VMPN** (Excel outline grouping; CSV blank separators) |
| Column picker | Metadata-driven filename from query/mode/filters |
| Role-gated pricing | Wholesale / cost / MSRP stripped for restricted roles |
| Shared gate | Grouped export uses same `availableColumns()` path as flat (FLSP-508 fix) |
| Tests | Export helpers in `verify:ci` |

Earlier foundation: FLSP-416 export, FLSP-495 role-gated print/export, original print button under FLSP-388.

## Explicitly deferred

See ADR [[decisions/clearview-approach-export-scope.md]]:

- PDF export
- Multi-pivot Approach templates (grand totals, DC-stock-by-manufacturer, location exception reports, location-based sorting)

Discovery docs (FLSP-109 PDF + SharePoint workshop) flag which templates are critical vs nice-to-have as **unresolved** — deferred work should start from that list, not re-discover.

## Architecture notes

- Export path: dedicated `export=1` query with slim select; images-first ordering via matviews
- Auth/RBAC: [[integrations/clearview-entra-sso.md]]
- Performance: parallel client fetches of capped pages; not a full Approach daily-batch refresh model — ClearView exports the **current filtered result set** from the RDS read plane

## Status

**Done** under FLSP-383. Future Approach-parity tickets should cite the deferred list above.
