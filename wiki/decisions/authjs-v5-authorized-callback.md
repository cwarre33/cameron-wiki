---
title: "ADR: Auth.js v5 Authorized Callback Trap"
type: decision
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_auth_gating_regression.md
  - raw/fls-work/clearview-memory/2026-07-21/reference_minted_session_jwt.md
related:
  - "[[integrations/clearview-entra-sso.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[decisions/clearview-approach-export-scope.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [adr, authjs, nextauth, middleware, entra, clearview, security, furnitureland-south]
---

# ADR: Auth.js v5 Authorized Callback Trap

## Decision

When using Auth.js v5 wrapped middleware `auth((req) => { … })`, **always gate with an explicit `req.auth` check** (redirect to sign-in). Do **not** rely on the `authorized` callback alone — the wrapper path discards it.

## Context

Discovered 2026-07-16: staging and prod ClearView served pages and data APIs (e.g. `/api/inventory-search`) with **no session**. Root cause in `next-auth` 5.0.0-beta.31 `handleAuth`: when a user middleware function is present, branch order runs that function and **ignores** `authorized === false`.

Timeline:

1. FLSP-587 wrapped `proxy.ts` as `auth((req) => {…})` for last-query-cookie redirect
2. FLSP-648 removed cookie logic but kept `auth((req) => NextResponse.next())` — pure pass-through
3. Middleware still ran (manifest healthy); it never redirected
4. RBAC unit checks did not cover the middleware gate

## Options considered

| Option | Outcome |
|--------|---------|
| Revert to `export const proxy = auth` only | Loses ability to compose redirects/cookies in wrapper |
| **Keep wrapper; check `req.auth?.user` inside** | Restores gate; documents trap inline |
| Rely solely on `authorized` callback | **Fails** with wrapped form — confirmed in library source |

## Decision rationale

1. Wrapper form is useful for app-specific redirects — keep it, own the gate
2. Explicit check + inline comment prevents reintroduction
3. Verification: clean standalone build + curl expects **307 → /signin** for `/` and `/items`; `/api/health` stays ungated

## Outcome

- Fix shipped 2026-07-16 (`a6a457b`); staging Entra browser OK; prod curl via ALB gated
- ECS rolling deploy can show mixed 200/307 for ~2 min — expected, not a new auth bug
- Local authed tests can mint session JWT — see [[integrations/clearview-entra-sso.md]]
- Integration page: [[integrations/clearview-entra-sso.md]]
