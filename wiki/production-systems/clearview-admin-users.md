---
title: ClearView Admin Users / Role Overrides
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-30/
  - cameron-intake:2026-09-02-admin-users-roster
related:
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
  - "[[decisions/clearview-dev-role-admin-restrict.md]]"
  - "[[work-log/2026-07-30-four-week-lookback.md]]"
  - "[[work-log/2026-08-09-clearview-shop-rmf-sprint.md]]"
created: 2026-07-30
updated: 2026-09-02
confidence: high
tags: [clearview, rbac, admin, entra, furnitureland-south, adoption]
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

## Adoption snapshot (prod Admin Users, 2026-09-02)

Cameron pasted the live Users table (name / last seen / effective roles / override). Aggregates only in wiki — no email roster committed.

| Metric | Count |
|--------|------:|
| Users on Admin list | **76** |
| Active role overrides | **30** |
| Seen **today** (2026-09-02) | **14** |
| Seen last **7 days** | **~46** |
| Seen last **14 days** | **~67** |
| Explicit `shop` role | **9** |
| `beta_tester` | **12** |
| `admin` | **11** |

**Role prevalence** (a user can hold multiple; counts are membership hits, not unique people):

| Role | Users holding |
|------|-------------:|
| merchandising | ~31 |
| viewer | ~29 |
| sales_manager | ~17 |
| sales_associate | ~15 |
| beta_tester | 12 |
| admin | 11 |
| shop | 9 |

**Reading:** ClearView has a real multi-role production audience (merchandising + sales + shop), not just IT. Shop-role cohort is still small (9) vs merchandising; department Shop view/create grants remain behind `DEPARTMENT_SHOP_ROLES_ENABLED` until UAT flip. Same-day activity (14) is healthy for an internal ops tool.

⚠️ Does **not** yet answer PIE dual-run vs full replace, or Shop/RMF **request volume**.
