---
title: ClearView Admin Users / Role Overrides
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-30/
related:
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
created: 2026-07-30
updated: 2026-07-30
confidence: high
tags: [clearview, rbac, admin, entra, furnitureland-south]
---

# ClearView Admin Users / Role Overrides

Admin panel: hide by role and ship **Users override** page for effective-role management.

**Status:** Done (including last-seen freshen via throttled session touch)

## Design decisions (locked 2026-07-24)

- Override edit UX: **modal** (export-dialog overlay pattern), not inline expand or `/admin/users/[id]`
- Role picker may grant **all** app roles including `admin`
- Users list: single fetch + client-side search (no server pagination) for small/medium scale
- Read model: one aggregated SQL (`app_users` + cached roles + overrides → `effective_roles`)

## Override propagation (deliberate non-work)

Roles resolve at sign-in into the JWT; session `maxAge` capped at **8h** (`AUTH_SESSION_MAX_AGE_HOURS`). Auto Entra SSO users still re-resolve roles at least every 8h. Break-glass: rotate `AUTH_SECRET`.

**Decision:** no extra UI copy or real-time revocation in this story — existing session cap is sufficient. Documented so close-outs don't re-litigate it.
