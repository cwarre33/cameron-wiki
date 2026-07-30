---
title: Open Question — Zendesk Auth Deadlines (API tokens + OAuth)
type: open-question
status: active
visibility: fls-internal
sources:
  - raw/fls-work/jira/2026-07-21/cameron-reporter-catalog.md
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
created: 2026-07-21
updated: 2026-07-30
confidence: high
tags: [open-question, zendesk, oauth, busylight, maintenance, api-tokens]
---

# Open Question — Zendesk Auth Deadlines (API tokens Jul 2026 + OAuth Oct 2026)

**Deadlines:**
- **July 28, 2026** — Zendesk unused API token deactivation window (**Done**)
- **October 27, 2026** — OAuth access-token expiration for custom apps (BusyLight focus)

**Roles:** Reporter Cameron Warren · Assignee John Abdellmelk (BusyLight path)

Umbrella: [[initiatives/zendesk-automation-platform.md]].

## Live status (2026-07-30)

| Summary | Status |
|---------|--------|
| Zendesk auth changes — API tokens (Jul 28) + OAuth refresh (Oct 27) | **In Progress** |
| BusyLight token refresh for OAuth | Open |
| Address unused Zendesk API token deactivation | **Done** |

## Scope notes

Primary custom OAuth client still **BusyLight Agent**. Monitor vendor OAuth clients; Task Server / API-token integrations are a separate lane (Jul 28 token cleanup closed).

Treat **Oct 27, 2026** as the hard OAuth deadline regardless of any stale tracker due date.

## Scope

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
3. After any change: smoke-test BusyLight and document disposition (already compliant / upgrade planned / not needed).

## Done when

- BusyLight disposition documented
- Story closed, **or** follow-up created only if John needs FLS dev work
- This page → `status: archived` (or superseded by a production-system note) once closed

## Docs

- [OAuth refresh announcement](https://support.zendesk.com/hc/en-us/articles/9182123625370)
- [Implement OAuth in your application](https://developer.zendesk.com/documentation/api-basics/authentication/using-oauth-to-authenticate-zendesk-api-requests-in-a-web-app/)
- [Refresh tokens](https://developer.zendesk.com/documentation/api-basics/authentication/refresh-token/)
