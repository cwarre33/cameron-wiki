---
title: ClearView Entra SSO (Auth.js v5)
type: integration
status: active
visibility: fls-internal
sources:
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp383_build_phase.md
  - raw/fls-work/clearview-memory/2026-07-21/project_auth_gating_regression.md
  - raw/fls-work/clearview-memory/2026-07-21/reference_minted_session_jwt.md
  - raw/fls-work/clearview-memory/2026-07-21/project_flsp403_aws_hosting.md
related:
  - "[[production-systems/inventory-lookup-clearview.md]]"
  - "[[initiatives/flsp-103-inventory-lookup.md]]"
  - "[[production-systems/clearview-aws-hosting.md]]"
  - "[[production-systems/approach-reporting.md]]"
  - "[[decisions/authjs-v5-authorized-callback.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [clearview, entra, sso, authjs, nextauth, rbac, flsp-414, furnitureland-south]
---

# ClearView Entra SSO (Auth.js v5)

Microsoft Entra ID single sign-on for hosted ClearView staging/prod, with session roles driving pricing visibility and export column gating.

**Parent hub:** [[production-systems/inventory-lookup-clearview.md]]  
**Jira:** [FLSP-414](https://furniturelandsouth.atlassian.net/browse/FLSP-414) **Done**

## Purpose

Internal-only ClearView must not serve inventory/pricing APIs anonymously. Entra replaces ad-hoc auth; roles map to NetSuite employee context for RBAC.

## Story tree (all Done)

| Key | Scope |
|-----|-------|
| FLSP-490–496 | Entra auth, staging tables, role resolution, session roles, employee delta sync, API/UI gating, RBAC verification |
| FLSP-544 | Login page (Jaylon) |

## Architecture

| Layer | Choice |
|-------|--------|
| Library | Auth.js / NextAuth v5 (`next-auth` 5.x beta) |
| IdP | Microsoft Entra (OIDC); redirect URIs per env |
| Secrets | Entra client ID/secret/issuer in SSM for staging+prod; Terraform ignore_changes on values |
| Middleware | `proxy.ts` — must check `req.auth` explicitly when using wrapped `auth((req) => …)` form |
| Roles | Session carries roles; `DEV_AUTH_ROLE` elevates roles locally but does **not** create a session |
| Ungated | `/api/health` (and similar health probes) |

Hosting path: [[production-systems/clearview-aws-hosting.md]]. Export RBAC: [[production-systems/approach-reporting.md]].

## Critical trap (fixed)

Wrapped Auth.js middleware **discards** the `authorized` callback result — your wrapper owns the gate. Staging/prod briefly served full app + data APIs with no session until fixed 2026-07-16.

Full ADR: [[decisions/authjs-v5-authorized-callback.md]].

## Local testing without Entra

Mint an Auth.js JWT with the repo `AUTH_SECRET` (`encode` from `next-auth/jwt`, salt `authjs.session-token`, cookie `authjs.session-token` on http localhost). Useful for Playwright; verified against next-auth 5.0.0-beta.31 / Next 16.

## Status

FLSP-414 Done. Entra browser flow verified on staging; prod gated via ALB after deploy. Ongoing hosting bugs (e.g. sign-in video asset on FLSP-784) are separate from SSO core.
