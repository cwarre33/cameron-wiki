---
title: Decision — ClearView Dev Role and Admin Self-Edit
type: decision
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp860_write_back.md
  - raw/fls-work/clearview-memory/2026-09-02/project_flsp1206_role_permissions.md
  - raw/fls-work/inventory-lookup-docs/2026-09-02/
  - raw/fls-work/git/2026-09-02/inventory-lookup/adr-signals.json
related:
  - "[[production-systems/clearview-shop-rmf-requests.md]]"
  - "[[production-systems/clearview-admin-users.md]]"
  - "[[initiatives/pie-shop-replacement.md]]"
created: 2026-09-02
updated: 2026-09-02
confidence: high
tags: [decision, clearview, rbac, admin, shop]
---

# Decision — ClearView Dev Role and Admin Self-Edit

**Context:** Shop write-back and Admin Users needed a way for developers to exercise privileged paths without widening production Admin, and Admins should not freely edit each other's overrides.

**Decision:**

1. Add an **invisible `dev` role** for developer break-glass / tooling — not shown as a normal assignable shop persona.
2. Restrict **Admin** override editing so an Admin can only edit **their own** role overrides (not other Admins'), unless a later story widens that deliberately.
3. Department Shop **view vs create** tiers layer on top of the existing pilot `canAccessShop` gate without removing it.
4. Ship department grants behind **`DEPARTMENT_SHOP_ROLES_ENABLED`** (defaults `false`) so promotion to prod does not instantly open ~125 CS / ~48 Purchasing / etc. until UAT flip.

**Status:** Dev-role / Admin self-edit Done; department view/create Done + prod-promoted; flag still off; broader access testing still open.

**Consequences:** Pilot membership and department roles stay independent. Zendesk-linked Shop routes remain on the stricter access tier (customer PII). Don't conflate `canViewShop` with mutation rights. Design consultant requires NetSuite role **1042** + title match (not title alone).
