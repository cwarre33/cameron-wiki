---
title: Zendesk Shared Views Cleanup
type: production-system
status: active
visibility: fls-internal
sources:
  - raw/fls-work/zendesk-tools/2026-07-21-memory.md
  - raw/fls-work/jira/2026-07-21/cameron-assignee-catalog.md
  - jira:FLSI-2968
  - repo:Zendesk/ZendeskSharedViews
related:
  - "[[initiatives/zendesk-automation-platform.md]]"
  - "[[production-systems/crr-round-robin.md]]"
created: 2026-07-21
updated: 2026-07-21
confidence: high
tags: [zendesk, views, shared-views, agent-tools, furnitureland-south]
---

# Zendesk Shared Views Cleanup

Reorganization of org-wide Zendesk shared views so agents stop relying on personal views. Delivered under [FLSI-2968](https://furniturelandsouth.atlassian.net/browse/FLSI-2968) (**Done**, live 2026-07-21); CCS folder follow-on [FLSI-3020](https://furniturelandsouth.atlassian.net/browse/FLSI-3020) (**Done**).

**Repo:** `CleanDevEnvironment/Zendesk/ZendeskTools/ZendeskSharedViews/` (audit & reorganization tooling). Completed per memory **2026-03-03** (`views-proposal-2026-03-03.md`).

Umbrella: [[initiatives/zendesk-automation-platform.md]].

## Problem

Shared views were disorganized; teams defaulted to personal views. Need: review → remove/revise → folder structure → leadership approval.

## Zendesk API / admin notes

- `GET /api/v2/views?per_page=100` — paginate via `next_page`
- No `shared` boolean on view objects — org-wide when `restriction: null`
- Folders are naming convention only: `Folder::View Name` (no separate folder-create API)
- Admin path: Admin Center → Workspaces → Agent Tools → Views

## Final folder structure (implemented)

| Folder | Views | Notes |
|--------|-------|-------|
| My Work | 8 | Agent-personal, filtered to current_user |
| Customer Service | 8 | Was “CCS” in proposal; includes Customer Service Inbox Tickets |
| CI | 8 | Year suffixes removed (no “-2025”) |
| Escalations | 2 | Typo fixed: “Escalation Review” |
| Manufacturer | 2 | |
| Management | 3 | Supervisor View, Ticket Clean Up, Grandparent Tickets |
| Specialist | 6 | Includes FLS Shop Repair (kept shared) |
| Surveys | 3 | |
| Driver | 2 | Driver App Tickets retained by choice |

## Deviations from proposal

- “CCS” folder renamed to **Customer Service**
- “Customer Service Inbox Tickets” moved into Customer Service (not Ops)
- No **Ops** folder created
- “Driver App Tickets” kept (redundant subset of All Driver Tickets — intentional)
- “Tickets in Wrong Group” / “Awaiting Acknowledgement” not in final list

## Interview angles

- **Convention over API:** `Folder::Name` is the entire folder model
- **Stakeholder-driven retention:** keep redundant Driver view when ops prefers familiarity
