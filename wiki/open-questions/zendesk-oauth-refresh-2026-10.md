---
title: Open Question — Zendesk OAuth Token Refresh (Oct 2026)
type: open-question
status: active
visibility: fls-internal
sources:
  - jira:FLSM-24
  - jira:FLSM-27
  - raw/fls-work/jira/2026-07-21/cameron-reporter-catalog.md
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [open-question, zendesk, oauth, busylight, flsm, maintenance]
---

# Open Question — Zendesk OAuth Token Refresh (Oct 2026)

**Hard deadline:** October 27, 2026 — Zendesk enforces OAuth access-token expiration for custom apps (email #14829284). Apps must handle refresh tokens or break.

**Jira:** [FLSM-24](https://furniturelandsouth.atlassian.net/browse/FLSM-24) (story) · [FLSM-27](https://furniturelandsouth.atlassian.net/browse/FLSM-27) (BusyLight sub-task) · parent epic [FLSM-6](https://furniturelandsouth.atlassian.net/browse/FLSM-6) (Zendesk)

**Roles:** Reporter Cameron Warren · Assignee John Abdellmelk · replaces FLSP-257 (moved out of FLSP-67).

Umbrella context: [[initiatives/zendesk-automation-platform.md]].

## Live status (2026-07-21)

| Key | Type | Summary | Status |
|-----|------|---------|--------|
| [FLSM-24](https://furniturelandsouth.atlassian.net/browse/FLSM-24) | Story | Zendesk OAuth token refresh - custom apps (Oct 27, 2026) | **In Progress** |
| [FLSM-27](https://furniturelandsouth.atlassian.net/browse/FLSM-27) | Sub-task | Handle BusyLight token refresh for OAuth | **Open** |

Jira `duedate` on FLSM-24 is **2026-06-05** (stale vs Zendesk enforcement date). Treat **Oct 27, 2026** as the real deadline.

## Scope (from FLSM-24)

**In scope — FLS-owned custom OAuth clients:**

| Client | Identifier | Tokens (May 2026) | Status | Action |
|--------|------------|-------------------|--------|--------|
| **BusyLight Agent** | `busylight_agent` | **56** | Active | **Primary focus** — confirm/implement refresh |
| PrivateViewChecker | `privateviewchecker` | 0 | Inactive | None unless reactivated |
| ZIS Client | `zis_netsuite` | 0 | Inactive | None unless reactivated |

**Out of scope:** vendor OAuth clients (Popdock, Power BI, Copilot, Zendesk Outlook, etc.) — vendors handle their own refresh; Task Server / API-token integrations; Mitel softphone (not listed as OAuth client — confirm separately if needed).

## Open questions

1. Does BusyLight Agent already handle refresh tokens + access-token expiration?
2. If not, who owns the code change — John only, or FLS IT assist before Oct 27?
3. After any change: smoke-test BusyLight and document disposition on FLSM-24 (already compliant / upgrade planned / not needed).

## Done when

- BusyLight disposition documented on FLSM-24
- Ticket closed, **or** follow-up created only if John needs FLS dev work
- This page → `status: archived` (or superseded by a production-system note) once closed

## Docs

- [OAuth refresh announcement](https://support.zendesk.com/hc/en-us/articles/9182123625370)
- [Implement OAuth in your application](https://developer.zendesk.com/documentation/api-basics/authentication/using-oauth-to-authenticate-zendesk-api-requests-in-a-web-app/)
- [Refresh tokens](https://developer.zendesk.com/documentation/api-basics/authentication/refresh-token/)
