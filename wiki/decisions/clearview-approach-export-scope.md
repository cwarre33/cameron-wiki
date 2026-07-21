---
title: "ADR: ClearView Approach Export Scope (FLSP-508)"
type: decision
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp508_approach_reporting.md
  - raw/fls-work/clearview-memory/2026-07-21/reference_approach_report_docs.md
related:
  - "[[production-systems/approach-reporting.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[integrations/clearview-entra-sso.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [adr, clearview, approach, export, flsp-508, furnitureland-south]
---

# ADR: ClearView Approach Export Scope (FLSP-508)

## Decision

**Close FLSP-508** with CSV/XLSX flat + grouped-by-VMPN export, column picker, and a **shared** role-based pricing gate — **without** PDF export or multi-pivot Approach report templates.

## Context

Legacy Approach supports pivoting one search into grand-total / manufacturer / location / exception views and PDF output. Discovery docs (FLSP-109 + SharePoint workshop) leave open which templates are operationally critical. ClearView already had export foundations (FLSP-416 / FLSP-495); FLSP-508 closed a real gated-export bug (grouped path bypassed pricing visibility) and added tests.

## Options considered

| Option | Outcome |
|--------|---------|
| Full Approach parity (PDF + all pivots) | Large open-ended scope; discovery open questions unresolved |
| **Ship CSV/XLSX + shared RBAC gate; defer pivots/PDF** | Matches "keep it simple" stakeholder posture; closes pricing leak |
| Leave FLSP-508 open until pivots land | Blocks epic hygiene; conflates security fix with product expansion |

## Decision rationale

1. Deferred items map to discovery **open questions**, not hard requirements
2. Pricing-visibility bug on grouped export was a must-fix; shared `availableColumns()` is the correct gate
3. Future Approach work should start from the explicit deferred list, not re-scope from scratch

## Outcome

- FLSP-508 **Done** 2026-07-21 (PR #58)
- Deferred: PDF; grand-total / DC-stock-by-manufacturer / location exception / location-sorted pivots
- Product page: [[production-systems/approach-reporting.md]]
